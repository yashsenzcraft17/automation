# from twilio.rest import Client
# import requests
# import os
# from base64 import b64encode
# from PIL import Image
# import pytesseract
# import json
# from formating import OPENAIBusinesscardgpt
# import time
# import pymysql
# from datetime import datetime
#
# class TwilioImageProcessor:
#     def __init__(self, account_sid, auth_token, whatsapp_number, image_folder):
#         self.client = Client(account_sid, auth_token)
#         self.whatsapp_number = whatsapp_number
#         self.image_folder = image_folder
#
#     def delete_existing_files(self):
#         existing_files = os.listdir(self.image_folder)
#         for file_name in existing_files:
#             file_path = os.path.join(self.image_folder, file_name)
#             try:
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#                     print(f"Deleted existing file: {file_name}")
#             except Exception as e:
#                 print(f"Error deleting file: {file_name}, {str(e)}")
#
#     def download_images(self, num_images=2, max_retries=3):
#         downloaded_media_count = 0
#
#         messages = self.client.messages.list(from_=f"whatsapp:{self.whatsapp_number}")
#
#         for message in messages:
#             print(f"Processing message from: {message.from_}")
#
#             # Convert num_media to an integer
#             num_media = int(message.num_media)
#
#             if num_media > 0:
#                 # Check if the message has media (images)
#                 print(f"Message contains {num_media} media item(s)")
#
#                 # Access media using list() method
#                 media_list = message.media.list()
#
#                 for media in media_list:
#                     print(f"Media content type: {media.content_type}")
#s
#                     if media.content_type.startswith('image'):
#                         try:
#                             # Construct the image URL using Twilio API
#                             base_url = 'https://api.twilio.com'
#                             image_url = f"{base_url}{media.uri.replace('.json', '')}"
#
#                             # Download the image using requests with authentication headers
#                             headers = {
#                                 'Authorization': f'Basic {b64encode(f"{account_sid}:{auth_token}".encode()).decode()}'}
#                             response = requests.get(image_url, headers=headers, stream=True)
#                             response.raise_for_status()  # Raise an HTTPError for bad responses
#
#                             # Save the image to the folder
#                             image_filename = f"{image_folder}/{message.sid}_{media.sid}.jpg"
#                             with open(image_filename, 'wb') as image_file:
#                                 for chunk in response.iter_content(1024):
#                                     image_file.write(chunk)
#
#                             print(f"Saved image: {image_filename}")
#
#                             # Increment the downloaded media count
#                             downloaded_media_count += 2
#
#                             # Break out of the loop if the desired number of media files is reached
#                             if downloaded_media_count == 2:
#                                 break
#
#                         except requests.exceptions.RequestException as e:
#                             print(f"Error processing image: {str(e)}")
#
#                     else:
#                         print("Media is not an image")
#
#                 # Break out of the outer loop if the desired number of media files is reached
#                 if downloaded_media_count == 2:
#                     break
#             else:
#                 print("Message does not contain any media")
#
#         print("Finished processing messages")
#
#
# def extract_text_from_image(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)
#         return text
#     except Exception as e:
#         return str(e)
#
#
# def process_images(image_folder):
#     files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
#     latest_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(image_folder, x)), reverse=True)[:2]
#     paths = [os.path.join(image_folder, file) for file in latest_files]
#
#     extracted_texts = [extract_text_from_image(path) for path in paths]
#     formatted_text = "\n\n".join(extracted_texts)
#
#     GPT_Bus = OPENAIBusinesscardgpt()
#     result = GPT_Bus.business_card_text(formatted_text)
#
#     # Print the value of 'result' before attempting to load it
#     print("Result before loading as JSON:", result)
#
#     if result is not None and result.strip():
#         try:
#             json_result = json.loads(result)
#             json_message_body = json.dumps(json_result, indent=2)
#             return json_message_body
#         except json.decoder.JSONDecodeError as e:
#             print("Error decoding JSON:", e)
#     else:
#         print("No valid JSON data found.")
#
#     return None
#
# class MySQLConnector:
#     def __init__(self, dbname, user, password, host, port, ssl_ca_path):
#         self.conn = pymysql.connect(
#             db=dbname,
#             user=user,
#             passwd=password,
#             host=host,
#             port=port,
#             cursorclass=pymysql.cursors.DictCursor,
#             ssl={'ssl': {'ssl_ca': ssl_ca_path}}  # Specify the path to your CA certificate
#         )
#         self.cursor = self.conn.cursor()
#
#     def create_lead_request_table(self):
#         query = """
#         CREATE TABLE IF NOT EXISTS t_lead_request_detail (
#             lead_request_detail_id INT AUTO_INCREMENT PRIMARY KEY,
#             lead_channel_id INT,
#             lead_record_type VARCHAR(45),
#             first_name VARCHAR(45),
#             last_name VARCHAR(45),
#             phone VARCHAR(45),
#             mobile VARCHAR(45),
#             mail_id VARCHAR(45),
#             organization VARCHAR(45),
#             address VARCHAR(45),
#             city VARCHAR(45),
#             state VARCHAR(45),
#             zipcode VARCHAR(45),
#             country VARCHAR(45),
#             designation VARCHAR(45),
#             department VARCHAR(45),
#             location VARCHAR(45),
#             contacted_on DATETIME,
#             lead_capture_status_id INT,
#             reviewed_by VARCHAR(45),
#             reviewed_on DATETIME,
#             is_auto_approved INT,
#             is_posted INT,
#             created_by VARCHAR(45),
#             created_on DATETIME
#         );
#         """
#         self.cursor.execute(query)
#         self.conn.commit()
#
#     def insert_lead_request(self, lead_data):
#         query = """
#         INSERT INTO t_lead_request_detail (
#             lead_channel_id, lead_record_type, first_name, last_name,
#             phone, mobile, mail_id, organization, address, city, state, zipcode,
#             country, designation, department, location, contacted_on, lead_capture_status_id,
#             reviewed_by, reviewed_on, is_auto_approved, is_posted, created_by, created_on
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#
#         # Check if "Mobile" key exists in lead_data
#         mobile_value = str(lead_data.get("Mobile")[:45]) if lead_data.get("Mobile") else None
#         phone_value = str(lead_data.get("Phone", "")[:45]) if lead_data.get("Phone") is not None else None
#         email_value = str(lead_data.get("Email", "")[:45]) if lead_data.get("Email") is not None else None
#         lead_values = (
#             lead_data.get("lead_channel_id"),
#             lead_data.get("lead_record_type"),
#             str(lead_data.get("FirstName", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("LastName", "")[:45]),  # Truncate to 45 characters
#             phone_value,  # Use the value obtained above
#             mobile_value,  # Use the value obtained above
#             email_value,  # Truncate to 45 characters
#             str(lead_data.get("Company", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("Street", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("City", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("State", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("PostalCode", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("Country", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("Designation_custom__c", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("Department__c", "")[:45]),  # Truncate to 45 characters
#             str(lead_data.get("Location", "")[:45]) if lead_data.get("Location") is not None else None,
#             # Truncate to 45 characters
#             datetime.now(),
#             lead_data.get("lead_capture_status_id"),
#             str(lead_data.get("reviewed_by", "")[:45]),  # Truncate to 45 characters
#             datetime.now() if lead_data.get("reviewed_on") else None,
#             lead_data.get("is_auto_approved"),
#             lead_data.get("is_posted"),
#             str(lead_data.get("created_by", "")[:45]),  # Truncate to 45 characters
#             datetime.now()
#         )
#         print("Lead Values:", lead_values)
#
#         self.cursor.execute(query, lead_values)
#         self.conn.commit()
#
#         return self.cursor.lastrowid
#
# def send_twilio_message(client, twilio_number, recipient_number, json_message_body):
#     message = client.messages.create(
#         body=json_message_body,
#         from_=twilio_number,
#         to=recipient_number
#     )
#     print(f'Message sent with SID: {message.sid}')
#
# if __name__ == "__main__":
#     account_sid = 'AC3399d019010b54584f42c36e50e32483'
#     auth_token = 'a5c5278391a71863b405543192868112'
#     whatsapp_number = '+919111349808'
#     image_folder = 'received_images'
#     twilio_number = "whatsapp:+14155238886"
#     recipient_number = "whatsapp:+919111349808"
#
#     twilio_processor = TwilioImageProcessor(account_sid, auth_token, whatsapp_number, image_folder)
#     twilio_processor.delete_existing_files()
#     twilio_processor.download_images(num_images=2)
#
#     json_message_body = json.loads(process_images(image_folder))
#
#     client = Client(account_sid, auth_token)
#     send_twilio_message(client, twilio_number, recipient_number, json_message_body)
#
#     db_params = {
#         'dbname': 'db_projectx',
#         'user': 'dbuser',
#         'password': 'dbuser@123!',
#         'host': 'db-senzcraft-dev.mysql.database.azure.com',
#         'port': 3306,
#         'ssl_ca_path': 'C:\\Users\\yashv\\Downloads\\DigiCertGlobalRootCA.crt.pem'
#     }
#
#     mysql_connector = MySQLConnector(**db_params)
#     mysql_connector.create_lead_request_table()
#
#
#     lead_data = {
#         "lead_channel_id": 1,  # Replace with actual lead_channel_id
#         "lead_record_type": "Secondary Channel",  # Replace with actual lead_record_type
#         "FirstName": json_message_body.get("FirstName"),
#         "LastName": json_message_body.get("LastName"),
#         "Phone": json_message_body.get("Phone"),
#         "Mobile": json_message_body.get("Mobile"),
#         "Email": json_message_body.get("Email"),
#         "Company": json_message_body.get("Company"),
#         "Street": json_message_body.get("Street"),
#         "City": json_message_body.get("City"),
#         "State": json_message_body.get("State"),
#         "PostalCode": json_message_body.get("PostalCode"),
#         "Country": json_message_body.get("Country"),
#         "Designation_custom__c": json_message_body.get("Designation_custom__c"),
#         "Department__c": json_message_body.get("Department__c"),
#         "Location": json_message_body.get("Location"),
#         "lead_capture_status_id": 0,  # Replace with actual lead_status_id
#         "reviewed_by": "SomeUser",  # Replace with actual user
#         "reviewed_on": "2024-01-12T12:00:00",  # Replace with actual reviewed_on date
#         "is_auto_approved": 1,  # Replace with actual value
#         "is_posted": 1,  # Replace with actual value
#         "created_by": "SomeUser",  # Replace with actual user
#     }
#
#     # Assuming 'lead_data' is a dictionary containing the data from the response
#     lead_request_detail_id = mysql_connector.insert_lead_request(lead_data)
#     print(f"Data inserted successfully. ID: {lead_request_detail_id}")
#
