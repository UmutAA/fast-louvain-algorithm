import pandas as pd

def load_edge_list(file_path: str):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found in {file_path}")
        return None