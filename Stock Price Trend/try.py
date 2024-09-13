'''import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div element with class 'topgainers_data' which contains the data
    div_data = soup.find('div', {'class': 'bsr_table hist_tbl_hm'})
    rows = div_data.find_all('div', {'class': 'row'})

    data = []
    for row in rows:
        cols = row.find_all('div')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    df = pd.DataFrame(data, columns=['Company', 'Last Price', 'Change', '% Change', 'Volume', 'Buy Price', 'Sell Price', 'Buy Qty / Qty Traded', 'Sell Qty / Qty Traded'])
    return df

def main():
    st.title("Top Gainers in NSE")
    st.markdown("Data scraped from MoneyControl")

    url = "https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php"
    top_gainers_df = scrape_data(url)

    st.dataframe(top_gainers_df)

if __name__ == "__main__":
    main()'''


#table = soup.find('table', {'id': 'card cardscreen cardtable'})

#url = "https://ticker.finology.in/market/top-gainers"mbsnav


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_data_from_url(url, div_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []

    for item in soup.find_all('div', class_=div_class):
        data.append(item.text.strip())

    
    data = scrape_data_from_url(url, div_class)
    redefined_data = str(data)
    soup = BeautifulSoup(redefined_data, 'html.parser')
    rows = soup.find_all('tr')
    # Extract the text data from each row
    text_data = []
    for row in rows:
        text_data.append(row.get_text())
        lines = text_data.strip().split('\n')
        final_data = [line.split() for line in lines]

# Create a DataFrame
        columns = ['No.', 'Company', 'priceRs.', 'Change%']
        df = pd.DataFrame(final_data, columns=columns)

# Display the DataFrame
        print(df)

# Print the extracted text data
    

def save_to_csv(df, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Data'])
        for item in df:
            writer.writerow([item])



if __name__ == "__main__":
    url = 'https://ticker.finology.in/market/top-gainers'  # Replace this with the URL you want to scrape
    div_class = 'card cardscreen cardtable'  # Replace this with the class of the <div> element containing the 
# Extract the text data from each row


#save_to_csv(text_data, 'scraped_data.csv')
import streamlit as st
import pandas as pd

def main():
    st.title("Scraped Data Display")

    # Load the scraped data from the CSV file
    data = pd.read_csv('scraped_data.csv')

    # Display the data in a Streamlit table
    st.table(data)

if __name__ == "__main__":
    main()
