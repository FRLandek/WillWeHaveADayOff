import streamlit as st
from client import client
from datetime import date, timedelta

def call(zip, time):
    c = client()
    return c.main(zip, time)

def main():

    st.title("Will we have a day off? 🤔")
    st.write("Enter the information to find out!")

    st.divider()

    zip = int(st.number_input("Enter your ZIP Code", placeholder="Enter a 5 digit number...", value=60540.0, format="%0f",step=1.0))
    time = st.date_input("Enter the date you want to check", value="today", min_value="today", format="MM/DD/YYYY")

    if time > date.today() + timedelta(days=6):
        st.warning("Checking a date past 7 days from now may return inaccurate results!", icon="⚠️")

    if st.button("Go!", type="primary", shortcut="Enter"):
        tt, tw, tc, sv, iv, str_NWS = call(zip, time)
        # st.write("Temps (f):", tt)
        # st.write("Windchills (f):", tc)
        # st.write("Wind (mph):", tt)
        st.write("Exact NWS Data:")
        st.code(str_NWS)

        # str_NWS, percent, chance = call(zip, time)
        # st.subheader("Chance:")
        # st.subheader(percent)
        # st.subheader(chance)
        # st.write("Exact NWS Data:")
        # st.code(str_NWS)
main()


