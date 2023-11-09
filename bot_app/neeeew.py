import os
import json
import google.generativeai as palm

from summa import summarizer

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Retrieve the API key from the environment variables
api_key = "AIzaSyDUpUT9XGiMjYD5w2YhhqH_K9cgZtOhY2M"  # Replace with your actual API key

# Configure palm
palm.configure(api_key=api_key)

# Choose a model, there is 1 model available
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# Custom prompt to encourage longer responses
custom_prompt = "Suppose you are a lawyer and guide me about {topic} about United Kingdom so I can understand"

# Cache to store the generated responses for the current topic
response_cache = {}

# Cache to store the previous question for context
topic_1_cache = {}

# Chat history to store all questions and answers
chat_history = {}

# File paths for chat history and topic_1_cache
chat_history_file = "chat_history.json"
topic_1_cache_file = "topic_1_cache.json"

# Function to load chat history from a JSON file
def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save chat history to a JSON file
def save_chat_history(chat_history, file_path):
    with open(file_path, "w") as file:
        json.dump(chat_history, file)

# Function to load the topic_1_cache from a JSON file
def load_topic_1_cache(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save the topic_1_cache to a JSON file
def save_topic_1_cache(topic_1_cache, file_path):
    with open(file_path, "w") as file:
        json.dump(topic_1_cache, file)

# Function to delete the data in the topic_1_cache file
def delete_topic_1_cache(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def generate_brief(text):
    # Use the summa library for text summarization
    return summarizer.summarize(text, ratio=0.2)  # Adjust the ratio as needed

# Function to generate a PDF report
def generate_pdf_report(chat_history, pdf_filename):
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Create a list to hold the content of the PDF
    content = []

    # Create a style for the table
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Add a title for the report
    content.append(Paragraph("Summary_Report", styles["Title"]))

    # Add the chat history as paragraphs
    for topic, chat in chat_history.items():
        if chat and "answer" in chat and chat["answer"]:
            content.append(Paragraph(f"Topic: {topic}", styles["Heading2"]))
            content.append(Paragraph(generate_brief(chat["answer"]), style))

    # Build the PDF document
    doc.build(content)

#sample function
def sample():
    #return to the route call
    return "this is the default response from sample func, "

# Main chatbot function
def chatbot(topic):
    chat_history = load_chat_history(chat_history_file)
    topic_1_cache = load_topic_1_cache(topic_1_cache_file)
    key = 1
    # while (key==1):
    #     # Get user input for the specific topic
    #     # topic = input("Enter a legal topic (or type 'exit' to end): ")

    #     if topic.lower() == 'exit':
    #         break

    #     # Check if the response is already in the cache
    #     if topic in response_cache:
    #         print("Legal Bot:", response_cache[topic])
    #         previous_question = topic_1_cache.get(topic, "")  # Get the previous question for context
    #         continue

    #     # Construct the API call prompt using the current topic and the previous question for context
    #     api_call_prompt = f"{custom_prompt} {topic}"
    #     if topic in topic_1_cache:
    #         previous_question = topic_1_cache[topic]
    #         api_call_prompt += f" {previous_question}"

    #     # Otherwise, generate the response and cache it
    #     response = palm.generate_text(
    #         prompt=api_call_prompt,
    #         model=model,
    #         temperature=0.95,
    #         max_output_tokens=2048,
    #         top_p=0.9,
    #         top_k=30,
    #         stop_sequences=["end of explanation"]
    #     )

    #     response_cache[topic] = response.result
    #     topic_1_cache[topic] = topic  # Store the current topic in topic_1_cache

    #     # Add the question and answer to the chat history
    #     chat_history[topic] = {"question": topic, "answer": response.result}

    #     print("Legal Bot:", response.result)

    # Save the chat history to a JSON file
    save_chat_history(chat_history, chat_history_file)
    save_topic_1_cache(topic_1_cache, topic_1_cache_file)

    # Generate the PDF report
    pdf_filename = "chat_history_report.pdf"
    generate_pdf_report(chat_history, pdf_filename)
    print(f"\nChat history saved to {chat_history_file}")
    print(f"Chat history report saved to {pdf_filename}")


    # Delete data in the topic_1_cache file
    delete_topic_1_cache(topic_1_cache_file)
    key = 0
    #return to the route call
    return "this is the default response from chatbot func"

# Run the chatbot
if __name__ == "__main__":
    chatbot()
