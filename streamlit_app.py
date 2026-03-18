import streamlit as st
from client import client
from datetime import date, timedelta

def call(zip, time, mock):
    c = client()
    if mock:
        return c.mockData()
    else:
        return c.main(zip, time)

def main():

    st.title("Will we have a day off? 🤔")
    st.write("Enter the information to find out!")

    st.divider()

    zip = int(st.number_input("Enter your ZIP Code", placeholder="Enter a 5 digit number...", value=60540.0, format="%0f",step=1.0))
    time = st.date_input("Enter the date you want to check", value="today", min_value="today", format="MM/DD/YYYY")

    if time > date.today() + timedelta(days=6):
        st.warning("Checking a date past 7 days from now may return inaccurate results!", icon="⚠️")

    with st.expander("Debug"):
        mock = st.checkbox("Mock Data")

    if st.button("Go!", type="primary", shortcut="Enter"):
        st.divider()

        #---- SHOWING ALL THE VALUES --------------
        # tt, tw, tc, sv, iv, str_NWS = call(zip, time, mock)
        # # st.write("Temps (f):", tt)
        # # st.write("Windchills (f):", tc)
        # # st.write("Wind (mph):", tt)
        # st.write("Snow:", sv)
        # st.write("National Weather Service Data (5-9 AM):")
        # st.code(str_NWS, language="text")


        #---- FINAL PRINT ------------------
        str_NWS, percent, chance = call(zip, time, mock)
        st.subheader("Chance:")
        st.subheader(percent)
        st.subheader(chance)
        st.write("Exact NWS Data:")
        st.code(str_NWS)
main()


