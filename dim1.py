import pandas as pd

df = pd.read_csv("HR_dataset_India.csv")

employee_dim = df[["Employee ID", "First Name", "Last Name", "Gender", "Birth Date"]].drop_duplicates()
employee_dim.to_csv("Employee_Dim.csv", index=False)

print("Employee_Dim.csv created successfully!")
