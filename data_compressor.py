import os
import pandas as pd

input_path = "dataloader/globalterrorismdb_0718dist.csv"
output_path = "dataloader/globalterrorismdb_small.parquet"

print("Loading file...")
df = pd.read_csv(input_path, encoding="latin1", low_memory=False)

required_cols = [
    "country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt", "nkill",
    "iyear", "nwound", "gname", "latitude", "longitude", "city","success", "suicide","summary"
]
df_filtered = df[required_cols]

print("Saving to Parquet...")
df_filtered.to_parquet(output_path, index=False, compression="snappy")

original_size = os.path.getsize(input_path) / (1024 * 1024)
new_size = os.path.getsize(output_path) / (1024 * 1024)

print("Process Complete")
print(f"Original Size: {original_size:.2f} MB")
print(f"New Size: {new_size:.2f} MB")
