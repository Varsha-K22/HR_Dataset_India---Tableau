import random
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

# -----------------------------
# Predefined Data
# -----------------------------
states_cities = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Delhi": ["New Delhi"],
    "West Bengal": ["Kolkata", "Darjeeling"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Telangana": ["Hyderabad", "Warangal"],
    "Kerala": ["Kochi", "Thiruvananthapuram"]
}

departments = {
    "HR": {"HR Manager": 0.4, "Recruiter": 0.6},
    "IT": {"Software Engineer": 0.5, "Data Analyst": 0.3, "System Admin": 0.2},
    "Finance": {"Accountant": 0.5, "Financial Analyst": 0.5},
    "Sales": {"Sales Executive": 0.7, "Sales Manager": 0.3},
    "Operations": {"Operations Executive": 0.6, "Operations Manager": 0.4}
}

education_mapping = {
    "HR Manager": "MBA",
    "Recruiter": "Bachelor's",
    "Software Engineer": "Bachelor's",
    "Data Analyst": "Master's",
    "System Admin": "Bachelor's",
    "Accountant": "Bachelor's",
    "Financial Analyst": "Master's",
    "Sales Executive": "Bachelor's",
    "Sales Manager": "MBA",
    "Operations Executive": "Bachelor's",
    "Operations Manager": "MBA"
}

performance_probs = {"Excellent": 0.2, "Good": 0.4, "Satisfactory": 0.3, "Needs Improvement": 0.1}

hire_year_probs = {2015:0.05, 2016:0.07, 2017:0.08, 2018:0.1, 2019:0.12, 2020:0.1, 
                   2021:0.12, 2022:0.12, 2023:0.12, 2024:0.12}

termination_year_probs = {2015:0.05, 2016:0.07, 2017:0.08, 2018:0.1, 2019:0.12, 2020:0.1, 
                          2021:0.12, 2022:0.12, 2023:0.12, 2024:0.12}

salary_ranges = {
    "HR Manager": (700000, 1200000),
    "Recruiter": (400000, 700000),
    "Software Engineer": (500000, 1200000),
    "Data Analyst": (600000, 1000000),
    "System Admin": (450000, 800000),
    "Accountant": (400000, 700000),
    "Financial Analyst": (600000, 1000000),
    "Sales Executive": (350000, 700000),
    "Sales Manager": (700000, 1200000),
    "Operations Executive": (400000, 700000),
    "Operations Manager": (700000, 1200000)
}

# -----------------------------
# Helper Functions
# -----------------------------
def weighted_choice(choices_dict):
    items = list(choices_dict.keys())
    probs = list(choices_dict.values())
    return np.random.choice(items, p=probs)

def random_hire_date():
    year = weighted_choice(hire_year_probs)
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    return fake.date_between(start, end)

def random_birth_date(hire_date, job_title):
    # Age ranges based on job seniority
    if "Manager" in job_title:
        age = random.randint(30, 55)
    else:
        age = random.randint(22, 40)
    birth_year = hire_date.year - age
    return fake.date_between_dates(datetime(birth_year, 1, 1), datetime(birth_year, 12, 31))

def random_termination_date(hire_date):
    if random.random() < 0.112:  # 11.2% chance
        year = weighted_choice(termination_year_probs)
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        term_date = fake.date_between(start, end)
        if term_date > hire_date + timedelta(days=180):  # at least 6 months after hire
            return term_date
    return None

def adjusted_salary(base_salary, gender, education, age):
    multiplier = 1.0
    if gender == "Female":
        multiplier *= 1.02  # small increment
    if education in ["Master's", "MBA"]:
        multiplier *= 1.1
    if age > 40:
        multiplier *= 1.05
    return int(base_salary * multiplier)

# -----------------------------
# Dataset Generation
# -----------------------------
records = []
for i in range(8950):
    emp_id = f"EMP{i+1:05d}"
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = np.random.choice(["Female", "Male"], p=[0.46, 0.54])
    state = random.choice(list(states_cities.keys()))
    city = random.choice(states_cities[state])
    hire_date = random_hire_date()
    department = weighted_choice({d:1/len(departments) for d in departments})
    job_title = weighted_choice(departments[department])
    education = education_mapping[job_title]
    performance = weighted_choice(performance_probs)
    overtime = np.random.choice(["Yes", "No"], p=[0.3, 0.7])
    salary = random.randint(*salary_ranges[job_title])
    birth_date = random_birth_date(hire_date, job_title)
    termination_date = random_termination_date(hire_date)
    adj_salary = adjusted_salary(salary, gender, education, (hire_date.year - birth_date.year))

    records.append([
        emp_id, first_name, last_name, gender, state, city, hire_date, department,
        job_title, education, performance, overtime, salary, birth_date, termination_date, adj_salary
    ])

# -----------------------------
# Save to CSV
# -----------------------------
columns = ["Employee ID", "First Name", "Last Name", "Gender", "State", "City", "Hire Date",
           "Department", "Job Title", "Education Level", "Performance Rating", "Overtime",
           "Salary", "Birth Date", "Termination Date", "Adjusted Salary"]

df = pd.DataFrame(records, columns=columns)
df.to_csv("HR_dataset_India.csv", index=False)

print("Dataset generated successfully with 8950 records!")
