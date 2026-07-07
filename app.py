import streamlit as st
st.title("mirai internship landing page")
st.write("Welcome to the Mirai Internship Program! Explore our opportunities and learn more about what we offer.")
user=st.text_input("Enter your name:")
if st.button("Submit"):
    st.write(user)