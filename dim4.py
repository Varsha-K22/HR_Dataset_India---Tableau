import pandas as pd

df = pd.read_csv("HR_dataset_India.csv")

location_dim = df[["State", "City"]].drop_duplicates().reset_index(drop=True)
location_dim["Location_ID"] = location_dim.index + 1
location_dim = location_dim[["Location_ID", "State", "City"]]

location_dim.to_csv("Location_Dim.csv", index=False)

print("Location_Dim.csv created successfully!")
