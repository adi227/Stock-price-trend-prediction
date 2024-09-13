import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data_from_url(url, div_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []

    for item in soup.find_all('div', class_=div_class):
        data.append(item.text.strip())

    # Reformat the scraped data into a DataFrame
    lines = data[0].strip().split('\n')
    final_data = [line.split() for line in lines]
    columns = ['No.', 'Company', 'priceRs.', 'Change%']
    df = pd.DataFrame(final_data, columns=columns)

    # Drop the rows containing "NA" values
    #df = df.dropna()

    # Reshape the DataFrame to have 4 columns
    num_rows = df.shape[0]
    num_cols = 4
    new_rows = num_rows // num_cols
    df = df.iloc[:new_rows * num_cols].reset_index(drop=True)
    df.columns = columns

    return df

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

import streamlit as st

def main():
    st.title("Scraped Data Display")

    url = 'https://ticker.finology.in/market/top-gainers'  # Replace this with the URL you want to scrape
    div_class = 'card cardscreen cardtable'  # Replace this with the class of the <div> element containing the data
    
    # Scrape data from the URL and create a DataFrame
    df = scrape_data_from_url(url, div_class)

    # Save the DataFrame to a CSV file
    save_to_csv(df, 'scraped_data.csv')

    # Display the data in a Streamlit table
    st.table(df)

if __name__ == "__main__":
    main()
