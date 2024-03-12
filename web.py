from twilio.rest import Client
import requests
import os
from base64 import b64encode
from PIL import Image
from formating import OPENAIBusinesscardgpt
import pytesseract
import json


# Your existing OPENAIBusinesscardgpt and other imports go here

# Twilio credentials
account_sid = 'AC3399d019010b54584f42c36e50e32483'
auth_token = 'a5c5278391a71863b405543192868112'
whatsapp_number = '+919111349808'

# Initialize Twilio client
client = Client(account_sid, auth_token)

def download_and_save_chats(client, whatsapp_number, num_chats_to_download, output_file):
    # Retrieve messages sent from a specific WhatsApp user
    messages = client.messages.list(from_=f"whatsapp:{whatsapp_number}")

    # Track the number of downloaded chat messages
    downloaded_chats_count = 5

    with open(output_file, 'w', encoding='utf-8') as file:
        for message in messages:
            print(f"Processing message from: {message.from_}")

            # Extract the text content of the message
            message_body = message.body

            # Save the message text to the file
            file.write(f"From: {message.from_}\n")
            file.write(f"Date: {message.date_created}\n")
            file.write(f"Message:\n{message_body}\n\n")

            # Increment the downloaded chats count
            downloaded_chats_count += 1

            # Break out of the loop if the desired number of chat messages is reached
            if downloaded_chats_count == num_chats_to_download:
                break

    print(f"Finished downloading {downloaded_chats_count} chat messages. Saved to {output_file}")

# Your desired number of chat messages to download
num_chats_to_download = 5

# Output file to save the chat messages
output_file = "downloaded_chats.txt"

# Define a folder to save images
image_folder = 'received_images'

# Remove existing files in the folder
existing_files = os.listdir(image_folder)
for file_name in existing_files:
    file_path = os.path.join(image_folder, file_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted existing file: {file_name}")
    except Exception as e:
        print(f"Error deleting file: {file_name}, {str(e)}")

os.makedirs(image_folder, exist_ok=True)

# Retrieve messages sent from a specific WhatsApp user
messages = client.messages.list(from_=f"whatsapp:{whatsapp_number}")

# Track the number of downloaded media files
downloaded_media_count = 0

for message in messages:
    print(f"Processing message from: {message.from_}")

    # Convert num_media to an integer
    num_media = int(message.num_media)

    if num_media > 0:
        # Check if the message has media (images)
        print(f"Message contains {num_media} media item(s)")

        # Access media using list() method
        media_list = message.media.list()

        for media in media_list:
            print(f"Media content type: {media.content_type}")

            if media.content_type.startswith('image'):
                try:
                    # Construct the image URL using Twilio API
                    base_url = 'https://api.twilio.com'
                    image_url = f"{base_url}{media.uri.replace('.json', '')}"

                    # Download the image using requests with authentication headers
                    headers = {'Authorization': f'Basic {b64encode(f"{account_sid}:{auth_token}".encode()).decode()}'}
                    response = requests.get(image_url, headers=headers, stream=True)
                    response.raise_for_status()  # Raise an HTTPError for bad responses

                    # Save the image to the folder
                    image_filename = f"{image_folder}/{message.sid}_{media.sid}.jpg"
                    with open(image_filename, 'wb') as image_file:
                        for chunk in response.iter_content(1024):
                            image_file.write(chunk)

                    print(f"Saved image: {image_filename}")

                    # Increment the downloaded media count
                    downloaded_media_count += 1

                    # Break out of the loop if the desired number of media files is reached
                    if downloaded_media_count == 2:
                        break

                except requests.exceptions.RequestException as e:
                    print(f"Error processing image: {str(e)}")

            else:
                print("Media is not an image")

        # Break out of the outer loop if the desired number of media files is reached
        if downloaded_media_count == 2:
            break
    else:
        print("Message does not contain any media")

# Your desired number of chat messages to download
num_chats_to_download = 10

# Output file to save the chat messages
output_file = "downloaded_chats.txt"

# Call the function to download and save chats
download_and_save_chats(client, whatsapp_number, num_chats_to_download, output_file)

# Continue with the rest of your code...

# Your Twilio phone number
twilio_number = "whatsapp:+14155238886"

# Recipient's phone number
recipient_number = "whatsapp:+919111349808"

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
# Read the chat file and extract lines containing "Message:"
extracted_chat_texts = []
with open(output_file, 'r', encoding='utf-8') as chat_file:
    inside_message = False
    current_message = ""

    for line in chat_file:
        if "Message:" in line:
            inside_message = True
            current_message = line.replace("Message:", "").strip()
        elif inside_message and line.strip() == "":
            inside_message = False
            extracted_chat_texts.append(current_message)
        elif inside_message:
            current_message += " " + line.strip()

# Print the extracted chat texts for verification
for chat_text in extracted_chat_texts:
    print("Extracted Chat Text:", chat_text)


# Concatenate the extracted text from chat messages into a single string
formatted_chat_text = "\n\n".join(extracted_chat_texts)
print(formatted_chat_text)

# Process the concatenated chat text
result_chat = GPT_Bus.business_card_text(formatted_chat_text)

# Print the value of result_chat
print("Result from GPT for chat messages:", result_chat)

# Convert the result to JSON format
try:
    json_result_chat = json.loads(result_chat)
    print("JSON Result:", json_result_chat)
except json.decoder.JSONDecodeError as e:
    print("Error decoding JSON:", e)


# Convert the result to JSON format
json_result_chat = json.loads(result_chat)


# Save the JSON result from chat messages to another text file
output_file_gpt_result_chat = "gpt_result_chats.txt"
with open(output_file_gpt_result_chat, 'w', encoding='utf-8') as json_file:
    json.dump(json_result_chat, json_file, indent=2)

# Convert the JSON result to a string for sending in the message
json_message_body = json.dumps(json_result, indent=2)


# Send the message with JSON result
message = client.messages.create(
    body=json_message_body,
    from_=twilio_number,
    to=recipient_number
    )

print(f'Message sent with SID: {message.sid}')
json_response_file_path = "json.txt"

# Write the JSON result to the text file
with open(json_response_file_path, 'w') as json_file:
    json.dump(json_result, json_file, indent=2)

print(f'JSON response saved to: {json_response_file_path}')
