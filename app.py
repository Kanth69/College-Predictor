from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load model + encoders
model, le_college, le_branch, le_category = pickle.load(open("model_clg_pred.pkl", "rb"))

# Load dataset (with official websites)
df = pd.read_csv("dataset.csv")  # columns: college, branch, category, website, round (optional)

# Prediction function
def predict_colleges_for_student(student_rank, student_category, student_branch, student_round, years=[2021,2022,2023,2024]):
    eligible_colleges = []

    # Encode inputs
    cat_enc = le_category.transform([student_category])[0]
    branch_enc = le_branch.transform([student_branch])[0]

    for college in df["college"].unique():
        try:
            college_enc = le_college.transform([college])[0]  # encode college
        except ValueError:
            continue  # skip if college not in encoder

        # Predict cutoff using all years
        predicted_ranks = []
        for year in years:
            X_input = [[college_enc, branch_enc, cat_enc, year, student_round]]
            pred_rank = model.predict(X_input)[0]
            predicted_ranks.append(pred_rank)

        max_rank = max(predicted_ranks)

        if student_rank <= max_rank:
            website = df[df["college"] == college]["website"].iloc[0]
            eligible_colleges.append((college, student_branch, int(max_rank), website))

    # Sort by predicted rank
    eligible_colleges = sorted(eligible_colleges, key=lambda x: x[2])

    # Remove duplicates
    seen = set()
    final_list = []
    for col in eligible_colleges:
        if col[0] not in seen:
            final_list.append(col)
            seen.add(col[0])

    return final_list

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        rank = int(request.form["rank"])
        branch = request.form["branch"]
        category = request.form["category"]
        round_number = int(request.form["round"])

        eligible_colleges = predict_colleges_for_student(rank, category, branch, round_number)

        return render_template("result.html", colleges=eligible_colleges, branch=branch)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
