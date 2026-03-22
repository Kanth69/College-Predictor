import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

# -----------------------------
# 1️⃣ Load dataset
# -----------------------------
df = pd.read_csv("dataset.csv")  # dataset with columns: year, college, branch, category, round, closing_rank, website

# -----------------------------
# 2️⃣ Encode categorical columns for model
# -----------------------------
le_college = LabelEncoder()
le_branch = LabelEncoder()
le_category = LabelEncoder()

df["college_enc"] = le_college.fit_transform(df["college"])
df["branch_enc"] = le_branch.fit_transform(df["branch"])
df["category_enc"] = le_category.fit_transform(df["category"])

# -----------------------------
# 3️⃣ Features and target
# -----------------------------
X = df[["college_enc", "branch_enc", "category_enc", "year", "round"]]
y = df["closing_rank"]

# -----------------------------
# 4️⃣ Train Random Forest Regressor
# -----------------------------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)
print("✅ Model trained successfully")

# Save model + encoders for future use
with open("model_clg_pred.pkl", "wb") as f:
    pickle.dump((model, le_college, le_branch, le_category), f)

# -----------------------------
# 5️⃣ Function to suggest colleges
# -----------------------------
def predict_colleges_for_student(student_rank, student_category, student_branch, student_round, years=[2021,2022,2023,2024]):
    """
    Predict eligible colleges for a student based on rank, category, branch, and round.
    Returns colleges sorted by increasing predicted closing rank with their websites.
    """
    eligible_colleges = []

    # Encode input values
    cat_enc = le_category.transform([student_category])[0]
    branch_enc = le_branch.transform([student_branch])[0]

    for year in years:
        for college_enc in df["college_enc"].unique():
            # Prepare input
            X_input = [[college_enc, branch_enc, cat_enc, year, student_round]]
            predicted_closing_rank = model.predict(X_input)[0]

            # Student eligible if rank <= predicted closing rank
            if student_rank <= predicted_closing_rank:
                college_name = le_college.inverse_transform([college_enc])[0]
                website = df[df["college"] == college_name]["website"].iloc[0]
                eligible_colleges.append((college_name, year, int(predicted_closing_rank), website))

    # Remove duplicates by college (keep the lowest predicted closing rank)
    eligible_colleges = sorted(eligible_colleges, key=lambda x: x[2])
    seen = set()
    final_list = []
    for col in eligible_colleges:
        if col[0] not in seen:
            final_list.append(col)
            seen.add(col[0])

    return final_list

# -----------------------------
# 6️⃣ Example usage
# -----------------------------
student_rank = 2000
student_category = "2A"
student_branch = "CSE"
student_round = 1

eligible_colleges = predict_colleges_for_student(student_rank, student_category, student_branch, student_round)

print("\n✅ Eligible Colleges (sorted by predicted closing rank):\n")
for college, year, closing_rank, website in eligible_colleges[:20]:
    print(f"{college} ({year}) - Predicted closing rank: {closing_rank} - Website: {website}")
