'''import os
from twilio.rest import Client
import datetime
from datetime import date

# Your Twilio account SID and AUTH Token, which can be found in the Twilio console
account_sid = "AC3cc22f330c589a185af4512896fbbad5"
auth_token = "fa99601298c7bd1dd77c29269bb34b39"
phone_number = input("Enter your phone number in format +91xxxxxxxxxx:" )
date_of_repayment=  input("Enter the date of Repayment of loan:")
x = date.today()
# Create a Twilio client
if int(date_of_repayment) == int(x.day):
  client = Client(account_sid, auth_token)

  message = client.messages.create(
  body="Time to repay your loan! Please make your payment by the due date to avoid any late fees. Let's stay on track with our financial commitments. Thank you.",
  from_="+15714102967",
  to=phone_number
)'''
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
