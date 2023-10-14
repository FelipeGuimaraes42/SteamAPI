import argparse
import os
import pandas as pd

from utils.dataframe_manipulation import *

# Example of how to use:
# python concat_dfs.py <path_to_df1> <path_to_df2>

def process_dataframes(df1_path, df2_path):
    if not (os.path.exists(df1_path) and os.path.exists(df2_path)):
        print("One or both input files do not exist.")
        return

    # Read data from the files into dataframes
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    concatenated_df = pd.concat([df1, df2])
    concatenated_df.set_index('steamid', inplace=True)
    concatenated_df = concatenated_df[~concatenated_df.index.duplicated(keep='first')]
    concatenated_df = dropUnnecessaryColumns(concatenated_df)

    # Save results
    concatenated_df.to_parquet(f"temp_concat.parquet", index=True)
    print(f"Data saved as a temporary file: 'temp_concat'")
    print(
        "If you'd like to version it, all you have to do is remove 'temp_' from its name."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatenate and process two dataframes")
    parser.add_argument("df1_path", help="Path to the first dataframe file")
    parser.add_argument("df2_path", help="Path to the second dataframe file")

    args = parser.parse_args()
    df1_path = args.df1_path
    df2_path = args.df2_path

    process_dataframes(df1_path, df2_path)
