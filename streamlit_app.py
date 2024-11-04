import streamlit as st
import openai
from langchain_core.runnables import RunnableBranch, RunnableLambda

# Set OpenAI API key from StreamLit secrets
openai.api_key = st.secrets["OpenAIkey"]

# Title of the app
st.title("Airline Feedback")

# Input box for user feedback
user_feedback = st.text_input("Share with us your experience of the latest trip:")

# Function to get sentiment analysis and responsibility classification from OpenAI
def analyze_feedback(feedback):
    try:
        # Use OpenAI to classify the feedback
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes customer feedback for an airline."},
                {"role": "user", "content": f"Classify the following feedback as positive or negative. If negative, indicate if the issue is due to the airline (e.g., lost luggage) or an external factor (e.g., weather-related delay). Feedback: {feedback}"}
            ]
        )
        
        # Extract content from the response
        classification = response['choices'][0]['message']['content'].strip().lower()
        return classification
    except Exception as e:
        st.write("We are having an error processing your feedback. Please try again later.")
        return None

# Define the response functions
def positive_response(input_text):
    return "Thank you for your positive feedback and for choosing to fly with us!"

def airline_fault_response(input_text):
    return "We're sorry for the inconvenience caused by the airline. Customer service will contact you soon to resolve the issue or provide compensation."

def external_issue_response(input_text):
    return "We're sorry to hear about the inconvenience. Unfortunately, this issue was beyond our control, and we cannot take responsibility for it."

# Set up a RunnableBranch to determine the appropriate response based on the classification
branch = RunnableBranch(
    branches=[
        (lambda classification: "positive" in classification, RunnableLambda(positive_response)),
        (lambda classification: "negative airline" in classification, RunnableLambda(airline_fault_response)),
        (lambda classification: "negative external" in classification, RunnableLambda(external_issue_response)),
    ],
    default=RunnableLambda(lambda x: "Thank you for your feedback!")
)

# Process and display response based on user input
if user_feedback:
    # Analyze the feedback to classify sentiment and responsibility
    classification = analyze_feedback(user_feedback)
    if classification:
        # Use RunnableBranch to determine the appropriate response
        response = branch.invoke(classification)
        st.write(response)
