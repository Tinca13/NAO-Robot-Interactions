import pandas as pd

def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df

if __name__ == "__main__":
    csv = "robot_commands.csv"
    df = load_csv(csv)
    print(df['command'].to_string(index=False))