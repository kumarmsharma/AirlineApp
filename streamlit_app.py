import streamlit as st
import openai
from langchain_core.runnables import RunnableBranch, RunnableLambda

# Set up your OpenAI API key from StreamLit secrets
openai.api_key = st.secrets["OpenAIkey"]

# Title of the app
st.title("Airline Feedback")

# Input box for user feedback
user_feedback = st.text_input("Share with us your experience of the latest trip:")

# Define response lambdas for each feedback type
def positive_response(input_text):
    return "Thank you for your positive feedback and for choosing to fly with us!"

def airline_fault_response(input_text):
    return "We're sorry for the inconvenience caused by the airline. Customer service will contact you soon to resolve the issue or provide compensation."

def external_issue_response(input_text):
    return "We're sorry to hear about the inconvenience. Unfortunately, this issue was beyond our control, and we cannot take responsibility for it."

# Set up a RunnableBranch to determine the appropriate response
branch = RunnableBranch(
    branches=[
        (lambda text: "bad" in text and "airline" in text, RunnableLambda(airline_fault_response)),
        (lambda text: "bad" in text and "weather" in text, RunnableLambda(external_issue_response)),
        (lambda text: "good" in text, RunnableLambda(positive_response))
    ],
    default=RunnableLambda(lambda x: "Thank you for your feedback!")
)

# Display response based on user input
if user_feedback:
    response = branch.invoke(user_feedback)
    st.write(response)
