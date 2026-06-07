import pandas as pd

df = pd.read_csv("HR_dataset_India.csv")

job_dim = df[["Job Title", "Department", "Education Level"]].drop_duplicates().reset_index(drop=True)
job_dim["JobTitle_ID"] = job_dim.index + 1
job_dim = job_dim[["JobTitle_ID", "Job Title", "Department", "Education Level"]]

job_dim.to_csv("JobTitle_Dim.csv", index=False)

print("JobTitle_Dim.csv created successfully!")
