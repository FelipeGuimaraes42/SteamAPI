import argparse
import pandas as pd

def csv_to_parquet(csv_file_path):
    try:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(csv_file_path)
        df.to_parquet('temp_optimized_df.parquet', index=True)
        print(f"CSV file has been successfully converted and saved as a Parquet file at 'temp_optimized_df.parquet'")
    except FileNotFoundError:
        print("The specified CSV file does not exist. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to a Parquet file")
    parser.add_argument("csv_file_path", help="Path to the input CSV file")

    args = parser.parse_args()
    csv_file_path = args.csv_file_path

    csv_to_parquet(csv_file_path)
