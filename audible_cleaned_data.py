import pandas as pd
import re

# Read data from CSV file
df = pd.read_csv('Audible_books_pagination.csv')

# Data cleaning steps
# Remove unnecessary prefixes
df['Writer'] = df['Writer'].str.replace('Written by: ', '')
df['Length'] = df['Length'].str.replace('Length: ', '')
df['Title'] = df['Title'].str.replace(r'\d+\.\s+', '', regex=True)  # Explicitly set regex=True
df['Narrator'] = df['Narrator'].str.replace('Narrated by: ', '')
df['Release Date'] = df['Release Date'].str.replace('Release Date: ', '')
df['Language'] = df['Language'].str.replace('Language: ', '')
df['Ratings'] = df['Ratings'].str.replace(' ratings ', '')

# Handle special characters using str.normalize
df['Writer'] = df['Writer'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Extract numerical values for length
def extract_length_minutes(length_str):
    matches = re.findall(r'\d+', length_str)
    minutes = int(matches[0]) if matches else 0
    hours = int(matches[1]) if len(matches) > 1 else 0
    return hours * 60 + minutes

df['Length'] = df['Length'].apply(extract_length_minutes)

# Adjust title to remove numeric prefixes
df['Title'] = df['Title'].apply(lambda x: x.split('. ', 1)[-1])

# Extract numeric ratings
def extract_numeric_rating(rating_str):
    try:
        return float(rating_str.split()[0])
    except ValueError:
        return None

df['Ratings'] = df['Ratings'].apply(extract_numeric_rating)

# Save cleaned dataset to a new CSV file
df.to_csv('Audible_books_Cleaned_Data.csv', index=False)
