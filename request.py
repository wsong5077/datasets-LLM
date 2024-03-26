import requests
import pandas as pd

# Make a GET request to fetch the data
response = requests.get('http://127.0.0.1:5000/paintings')

# Ensure the request was successful
if response.status_code == 200:
    paintings_data = response.json()
    print(paintings_data)

    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(paintings_data)
    print(df)

    # Optionally, save the DataFrame to a CSV file
    df.to_csv('paintings_data.csv', index=False)
else:
    print(f"Failed to fetch data: {response.status_code}")
