from twilio.rest import Client
import json
from PIL import Image
import pytesseract
from buisness import OPENAIBusinesscardgpt
import os

# Your Twilio account SID and auth token
account_sid = 'AC3399d019010b54584f42c36e50e32483'
auth_token = 'a5c5278391a71863b405543192868112'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Your Twilio phone number
twilio_number = "whatsapp:+14155238886"

# Recipient's phone number
recipient_number = "whatsapp:+919940077131"

# Define the path for each business card image
folder_path = "C:\\Users\\yashv\\PycharmProjects\\bank_project\\received_images"

# Get a list of all files in the folder
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Generate paths for all images in the folder
paths = [os.path.join(folder_path, file) for file in files]

# Function to extract text from an image
def extract_text_from_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return str(e)

# Extract text from each business card
extracted_texts = [extract_text_from_image(path) for path in paths]

# Concatenate the extracted text into a single string
formatted_text = "\n\n".join(extracted_texts)

# Create an instance of the OPENAIBusinesscardgpt class
GPT_Bus = OPENAIBusinesscardgpt()

# Process the concatenated text
result = GPT_Bus.business_card_text(formatted_text)

# Convert the result to JSON format
json_result = json.loads(result)

# Convert the JSON result to a string for sending in the message
json_message_body = json.dumps(json_result, indent=2)

# Send the message with JSON result
message = client.messages.create(
    body=json_message_body,
    from_=twilio_number,
    to=recipient_number
)

print(f'Message sent with SID: {message.sid}')
