import streamlit as st

# Title of the app
st.title("Airline Feedback")

# Input box for user feedback
user_feedback = st.text_input("Share with us your experience of the latest trip:")

# Define a function to determine response based on feedback
def get_feedback_response(feedback):
    if "bad" in feedback:
        if "airline" in feedback or "luggage" in feedback:
            return "We're sorry for the inconvenience caused by the airline. Customer service will contact you soon to resolve the issue or provide compensation."
        elif "weather" in feedback or "delay" in feedback:
            return "We're sorry to hear about the inconvenience. Unfortunately, this issue was beyond our control, and we cannot take responsibility for it."
    elif "good" in feedback or "great" in feedback:
        return "Thank you for your positive feedback and for choosing to fly with us!"
    return "Thank you for your feedback!"

# Display response based on user input
if user_feedback:
    response = get_feedback_response(user_feedback)
    st.write(response)
