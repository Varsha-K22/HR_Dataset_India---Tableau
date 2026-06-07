import pandas as pd

df = pd.read_csv("HR_dataset_India.csv")

education_dim = df[["Education Level"]].drop_duplicates().reset_index(drop=True)
education_dim["Education_ID"] = education_dim.index + 1
education_dim = education_dim[["Education_ID", "Education Level"]]

education_dim.to_csv("Education_Dim.csv", index=False)

print("Education_Dim.csv created successfully!")
