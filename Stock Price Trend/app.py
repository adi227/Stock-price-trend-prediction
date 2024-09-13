import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from keras.models import load_model
import streamlit as st


start_date = datetime.datetime.now() - datetime.timedelta(days=365 * 10)  # 10 years ago
end_date = datetime.datetime.now()


ticker = "AAPL"  
st.title('Stock Trend Prediction')
user_input = st.text_input('Enter Stock Ticker','AAPL')
# Fetch the data from Yahoo Finance
df = yf.download(user_input, start=start_date, end=end_date)#Alternate df = pdr.DataReader(ticker, 'yahoo', start_date, end_date)

#Describing the data
st.subheader('Data from 2013-2023')
st.write(df.describe())

#Visualizations
st.subheader('Closing price vs Time chart')
fig = plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)


st.subheader('Closing price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)


#splitting Data into Training and Testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

print(data_training.shape)
print(data_testing.shape)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)


#load my model
model = load_model('keras_model.h5')

#Testing part
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)


x_test = []
y_test = []

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])
x_test,y_test = np.array(x_test),np.array(y_test)
y_predicted = model.predict(x_test)


scaler = scaler.scale_
scale_factor = 1/scaler[0]

y_predicted = y_predicted*scale_factor
y_test = y_test*scale_factor


#Final Graph
st.subheader('Predicted Value vs Original Value')

fig2 = plt.figure(figsize =(12,6) )
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)


#Twilio reminder
import streamlit as st
import pandas as pd
from twilio.rest import Client
from datetime import datetime, timedelta

# Your Twilio credentials
TWILIO_ACCOUNT_SID = "AC3cc22f330c589a185af4512896fbbad5"
TWILIO_AUTH_TOKEN = "fa99601298c7bd1dd77c29269bb34b39"
TWILIO_PHONE_NUMBER = "+15714102967"
USER_PHONE_NUMBER = "+919979887599"

# Function to send the reminder using Twilio
def send_twilio_message(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(to=USER_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=message)

def main():
    st.header("Mutual Fund Reminder ")
    

    # Get user inputs
    amount = st.number_input("Enter the investment amount:", min_value=1)
    date = st.date_input("Select the investment date:")
    User_number = st.number_input("Enter your phone number:")
    if st.button("Set Reminder"):
        # Get the current date
        today = datetime.now().date()

        # Calculate the number of days until the investment date
        days_left = (date - today).days

        if days_left <= 0:
            st.error("Invalid date. Please select a future date.")
        else:
            # Store the reminder in a DataFrame
            data = pd.DataFrame({
                "Amount": [amount],
                "Investment Date": [date],
            })

            # Save the data to a CSV file
            data.to_csv("reminders.csv", index=False)

            # Send the reminder message
            message = f"Reminder: You have an upcoming mutual fund investment of {amount} on {date}."
            send_twilio_message(message)

            st.success("Reminder set! You will receive an SMS on the investment date.")

if __name__ == "__main__":
    main()
#Top Gainers from nifty

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
    st.title("Top Gainers of day")

    # Load the scraped data from the CSV file
    data = pd.read_csv('scraped_data.csv')

    # Display the data in a Streamlit table
    st.table(data)

if __name__ == "__main__":
    main()
