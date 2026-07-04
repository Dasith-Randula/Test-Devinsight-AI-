import pandas as pd
import json

# 1. Features load කරන්න
df_features = pd.read_csv('dataset_features.csv')

# 2. Labels load කරන්න
with open('buggy_labels.json', 'r') as f:
    buggy_dict = json.load(f)

# 3. 'is_buggy' column එක add කරන්න
def get_label(file_path):
    # file_path එක exact match වෙනවාද බලන්න
    if file_path in buggy_dict:
        return 1  # Buggy
    else:
        return 0  # Not buggy (or unknown)

df_features['is_buggy'] = df_features['file_path'].apply(get_label)

# 4. Final dataset එක save කරන්න
df_features.to_csv('final_dataset.csv', index=False)

print(f"✅ Final dataset created with {len(df_features)} files.")
print(df_features.head())
print(f"\n📊 Class distribution:")
print(df_features['is_buggy'].value_counts())