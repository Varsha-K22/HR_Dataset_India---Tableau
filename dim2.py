import pandas as pd

df = pd.read_csv("HR_dataset_India.csv")

department_dim = df[["Department"]].drop_duplicates().reset_index(drop=True)
department_dim["Department_ID"] = department_dim.index + 1
department_dim = department_dim[["Department_ID", "Department"]]

department_dim.to_csv("Department_Dim.csv", index=False)

print("Department_Dim.csv created successfully!")
