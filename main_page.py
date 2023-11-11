# APP to compute the center of mass of an investment position


import streamlit as st
import numpy as np
import yfinance as yf


def get_last_price(ticker: str) -> float:
    # Get the historical data for the last day
    historical_data = yf.download(ticker, period="1d")
    return historical_data["Close"].iloc[-1]


if __name__ == "__main__":
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")
    st.title("Center of Mass calculation")

    ticker = st.text_input("Enter the ticker for a index:")  # specificato dall'utente

    purchase_price_today = get_last_price(ticker)

    purchase_prices = np.array([5, 10, 15, 10])  # euro/stock --> d
    purchase_quantities = np.array([1000, 500, 800, 200])  # euro --> m

    com = np.dot(purchase_prices, purchase_quantities) / sum(purchase_quantities)
    com_relative = (purchase_price_today - com) / com
    st.write(f"The com of your current position is: {com}")
    st.write(f"The current price for {ticker} is {com_relative}% of your com")
