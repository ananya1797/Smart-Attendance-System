import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

# Get the current date and timestamp
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# Auto-refresh settings
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Display FizzBuzz counter logic
if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Construct file path using os.path.join
file_path = os.path.join("Attendance", f"Attendance_{date}.csv")

# Load and display the CSV file
try:
    df = pd.read_csv(file_path)
    st.dataframe(df.style.highlight_max(axis=0))
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
except Exception as e:
    st.error(f"An error occurred: {e}")
