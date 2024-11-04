import streamlit as st
import openai

# Set up OpenAI API key from StreamLit secrets
openai.api_key = st.secrets["OpenAIkey"]

# Title of the app
st.title("Airline Feedback")

# Input box for user feedback
user_feedback = st.text_input("Share with us your experience of the latest trip:")

# Function to classify feedback using OpenAI
def classify_feedback(feedback):
    try:
        # Use OpenAI's API to analyze the feedback
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that classifies feedback as positive, negative, or neutral and identifies if the issue is airline-related or due to external factors."},
                {"role": "user", "content": f"Classify this feedback: '{feedback}'"}
            ]
        )
        
        # Extract the response text
        analysis = response.choices[0].message['content'].strip().lower()

        # Determine response based on OpenAI analysis
        if "positive" in analysis:
            return "positive"
        elif "negative" in analysis and "airline-related" in analysis:
            return "negative_airline"
        elif "negative" in analysis and "external factor" in analysis:
            return "negative_external"
        else:
            return "neutral"
    except Exception as e:
        return "error"

# Function to generate response based on classification
def get_feedback_response(classification):
    if classification == "positive":
        return "Thank you for your positive feedback and for choosing to fly with us!"
    elif classification == "negative_airline":
        return "We're sorry for the inconvenience caused by the airline. Customer service will contact you soon to resolve the issue or provide compensation."
    elif classification == "negative_external":
        return "We're sorry to hear about the inconvenience. Unfortunately, this issue was beyond our control, and we cannot take responsibility for it."
    elif classification == "error":
        return "We're experiencing an issue processing your feedback. Please try again later."
    else:
        return "Thank you for your feedback!"

# Process feedback and display response
if user_feedback:
    classification = classify_feedback(user_feedback)
    response = get_feedback_response(classification)
    st.write(response)
