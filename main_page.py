# APP to compute the center of mass of an investment position


import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
from com_investing_logic.ComProcessor import ComProcessor


@st.cache_data
def get_last_price(ticker: str) -> float:
    # Get the historical data for the last day
    historical_data = yf.download(ticker, period="1d")
    return historical_data["Close"].iloc[-1]


def import_users_investments():
    st.title("Multiple Input Table App")

    # Input widget for the number of rows in the table
    num_rows = st.slider("Number of transactions", min_value=1, max_value=10, value=5)

    # Create a list to store user inputs
    input_data = []

    # Loop to get user inputs
    for i in range(num_rows):
        # Input widget for each column
        col1 = st.number_input(f"purchase price, transaction {i + 1}", key=f"col1_{i}")
        col2 = st.number_input(f"purchase qty  , transaction {i + 1}", key=f"col2_{i}")

        # Append the user inputs to the list
        input_data.append({"purchase price": col1, "purchase qty": col2})

    # Create a DataFrame from the input data
    df = pd.DataFrame(input_data)
    if df.empty:
        return
    else:
        return df


def main():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")
    st.title("Center of Mass calculation")

    ticker = st.text_input(
        "Enter the ticker for a index:",
    )

    if ticker:
        current_price = get_last_price(ticker)
        st.write(f"The current closing price for today is: {current_price:.1f}")

        df = import_users_investments()

        if not (df.empty):
            # Display the table

            st.table(df)
            price_array = df["purchase price"].values  # euro/stock --> d
            qty_array = df["purchase qty"].values  # euro --> m

            comProcessor = ComProcessor(current_price, price_array, qty_array)
            comProcessor.calculate_com()
            comProcessor.calculate_com_relative()

            st.write(f"The com of your current position is: {comProcessor.com:.1f}")
            st.write(
                f"The current price for {ticker} is {comProcessor.com_relative:.1f}% of your com"
            )


if __name__ == "__main__":
    main()
