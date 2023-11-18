import pandas as pd

# List of CSV file paths
csv_files = ['onion_fake_news.csv',
            'satirewire_biz_fake_news.csv',
            'satirewire_biz_briefs_fake_news.csv',
            'satirewire_sci-tech_fake_news.csv',
            'satirewire_scifi_briefs_fake_news.csv',
            'clickhole_fake_news2.csv',
            'clickhole_fake_news.csv']

# Load all CSV files into a list of DataFrames
dataframes = [pd.read_csv(file) for file in csv_files]

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('combined_fake_news.csv', index=False)

print("Combined CSV saved successfully.")
