import pandas as pd
import random

# ------------------ College List with official websites ------------------
colleges_info = {
    "RVCE": {"website": "https://www.rvce.edu.in"},
    "PES University": {"website": "https://pes.edu/"},
    "BMSCE": {"website": "https://www.bmsce.ac.in/"},
    "MSRIT": {"website": "https://www.msrit.edu/"},
    "UVCE": {"website": "https://uvce.ac.in/"},
    "SJCE Mysore": {"website": "https://sjce.ac.in/"},
    "BIT Bangalore": {"website": "https://bit-bangalore.edu.in/"},
    "DSCE": {"website": "https://www.dsce.edu.in/"},
    "RNSIT": {"website": "https://rnsit.ac.in/"},
    "SIT Tumkur": {"website": "https://sit.ac.in/"},
    "JSSATE Bangalore": {"website": "https://jssateb.ac.in/"},
    "KLE Tech Hubli": {"website": "https://kletech.ac.in/"},
    "BNMIT": {"website": "https://bnmit.org/"},
    "Nitte Meenakshi Institute": {"website": "https://nitte.edu.in/"},
    "MVJ College of Engineering": {"website": "https://mvjce.edu.in/"},
    "Sapthagiri College of Engineering": {"website": "https://sapthagiri.edu.in/"},
    "Global Academy of Technology": {"website": "https://gat.ac.in/"},
    "Presidency University": {"website": "https://presidencyuniversity.in/"},
    "Alliance University": {"website": "https://alliance.edu.in/"},
    "Oxford College of Engineering": {"website": "https://oxford.edu.in/"},
    "Dayananda Sagar Academy": {"website": "https://dsacademy.edu.in/"},
    "Don Bosco Institute of Technology": {"website": "https://dbit.ac.in/"},
    "Atria Institute of Technology": {"website": "https://atria.edu/"},
    "HKBK College of Engineering": {"website": "https://hkbk.edu.in/"},
    "East Point College of Engineering": {"website": "https://epce.edu.in/"},
    "Acharya Institute of Technology": {"website": "https://acharya.ac.in/"},
    "Reva University": {"website": "https://reva.edu.in/"},
    "NHCE": {"website": "https://nhce.edu.in/"},
    "CMRIT": {"website": "https://cmrit.ac.in/"},
    "KLS Gogte Institute": {"website": "https://gogteinstitutions.org/"},
    "SDM College": {"website": "https://sdmcet.ac.in/"},
    "MIT Manipal": {"website": "https://manipal.edu/"},
    "Canara Engineering College": {"website": "https://canaraengineering.in/"},
    "PES Mandya": {"website": "https://pesmandya.edu.in/"},
    "Vidya Vikas Institute": {"website": "https://vvit.ac.in/"},
    "BVB Hubli": {"website": "https://bvbhubli.edu.in/"},
    "AIT Chikmagalur": {"website": "https://aitchikmagalur.edu.in/"},
    "MS Engineering College": {"website": "https://msengineering.edu.in/"},
    "T John Institute of Technology": {"website": "https://tjohncollege.edu.in/"},
    "AMC Engineering College": {"website": "https://amc.edu.in/"},
    "Sri Venkateshwara College of Engineering": {"website": "https://svce.edu.in/"},
    "KSIT": {"website": "https://ksit.edu.in/"},
    "Sapthagiri Institute": {"website": "https://sapthagiri.edu.in/"},
    "CMR University School of Engineering": {"website": "https://cmr.edu.in/"},
    "Sri Siddhartha Institute": {"website": "https://ssit.edu.in/"},
    "Bangalore Institute of Technology North Campus": {"website": "https://bit.edu.in/"},
    "Ramaiah Institute of Technology": {"website": "https://msrit.edu/"},
    "Adichunchanagiri Institute": {"website": "https://acoe.edu.in/"},
    "Vemana Institute of Technology": {"website": "https://vemanait.edu.in/"},
    "PESIT RR": {"website": "https://pes.edu/"},
    "PESIT South": {"website": "https://pes.edu/"},
    "Sir MVIT": {"website": "https://sir-mvit.ac.in/"},
    "Vidyavardhaka College": {"website": "https://vvc.ac.in/"},
    "New Horizon College of Engineering": {"website": "https://newhorizon.edu.in/"},
    "BMSIT Bangalore": {"website": "https://bmsit.ac.in/"},
    "KSSEM Bangalore": {"website": "https://kssem.edu.in/"},
    "Brindavan College of Engineering": {"website": "https://brindavancollege.edu.in/"},
    "Dayananda Sagar College": {"website": "https://dsce.edu.in/"},
    "NIE Mysore": {"website": "https://nie.ac.in/"},
    "Siddaganga Institute": {"website": "https://sit.ac.in/"},
    "Vidya Jyothi Institute": {"website": "https://vji.ac.in/"},
    "JSS Science & Technology": {"website": "https://jssstuniv.in/"}
}

# ------------------ Settings ------------------
branches = ["CSE", "ISE", "ECE", "EEE", "MECH"]  # branch priority
categories = ["GM", "1", "2A", "2B", "3A", "3B", "SC", "ST"]  # category priority
rounds = [1, 2, 3]
years = [2021, 2022, 2023, 2024]

# Category factor (top-down: GM hardest, SC/ST easiest)
cat_factor = {
    "GM": 1.0,
    "1": 1.05,
    "2A": 1.1,
    "2B": 1.15,
    "3A": 1.2,
    "3B": 1.25,
    "SC": 1.5,
    "ST": 1.6
}

# Branch factor (CSE hardest, MECH easiest)
branch_factor = {
    "CSE": 1.0,
    "ISE": 1.05,
    "ECE": 1.1,
    "EEE": 1.15,
    "MECH": 1.2
}

# Base cutoff map in realistic top-down order
base_cutoff_ordered = [
    "RVCE", "PES University", "BMSCE", "MSRIT", "MIT Manipal", "UVCE", "SJCE Mysore",
    "NIE Mysore", "Siddaganga Institute", "BIT Bangalore", "DSCE", "BMSIT Bangalore",
    "RNSIT", "PESIT RR", "BNMIT", "JSSATE Bangalore", "Sir MVIT", "New Horizon College of Engineering",
    "PESIT South", "Acharya Institute of Technology", "CMRIT", "MVJ College of Engineering",
    "Reva University", "KLE Tech Hubli", "KSIT", "Oxford College of Engineering",
    "Sapthagiri College of Engineering", "East Point College of Engineering", "Canara Engineering College",
    "Vidyavardhaka College", "Vidya Vikas Institute", "Global Academy of Technology", "KSSEM Bangalore",
    "Presidency University", "Alliance University", "Sri Venkateshwara College of Engineering",
    "CMR University School of Engineering", "Sri Siddhartha Institute", "Adichunchanagiri Institute",
    "Vemana Institute of Technology", "AIT Chikmagalur", "MS Engineering College",
    "Vidya Jyothi Institute", "Don Bosco Institute of Technology", "Dayananda Sagar Academy",
    "T John Institute of Technology", "AMC Engineering College", "Bangalore Institute of Technology North Campus",
    "JSS Science & Technology"
]


# Assign realistic base cutoff ranks (smaller is better)
base_cutoff_map = {}
start_rank = 500  # top rank for best college
increment = 2000  # difference between consecutive colleges
for idx, college in enumerate(base_cutoff_ordered):
    base_cutoff_map[college] = start_rank + idx * increment

# ------------------ Generate dataset ------------------
data = []

for year in years:
    for college in base_cutoff_ordered:
        base_rank = base_cutoff_map[college]
        website = colleges_info[college]["website"]
        for branch in branches:
            b_factor = branch_factor[branch]
            for category in categories:
                c_factor = cat_factor[category]
                for rnd in rounds:
                    r_factor = 1 + 0.05 * (rnd - 1)  # round effect
                    noise = random.uniform(0.95, 1.05)
                    closing_rank = int(base_rank * b_factor * c_factor * r_factor * noise)
                    closing_rank = min(closing_rank, 200000)
                    data.append([year, college, branch, category, rnd, closing_rank, website])

# Create DataFrame
df = pd.DataFrame(data, columns=["year", "college", "branch", "category", "round", "closing_rank", "website"])

# Optional: shuffle if needed
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv("dataset.csv", index=False)
print("Dataset generated: dataset.csv with", df.shape[0], "rows")
print(df.head())
