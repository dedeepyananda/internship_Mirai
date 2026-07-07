import streamlit as st

st.title("Simple Calculator")
num1=st.number_input("Enter first number:", format="%.0f")
num2=st.number_input("Enter second number:", format="%.0f")
operation=st.selectbox("choose operation",("Addition","Subtraction","Multiplication","Division"))
if st.button("Calculate"):
    if operation == "Addition":
        st.write(f"Addition of {num1} and {num2} is {num1+num2}")
    elif operation == "Subtraction":
        st.write(f"Subtraction of {num1} and {num2} is {num1-num2}")
    elif operation == "Multiplication":
        st.write(f"Multiplication of {num1} and {num2} is {num1*num2}")
    elif operation == "Division":
        if num2 == 0:
            st.write("Division by zero is not allowed")
        else:
            st.write(f"Division of {num1} and {num2} is {num1/num2}")

