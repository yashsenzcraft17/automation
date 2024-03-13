# import json
# import requests
#
# # Salesforce credentials
# salesforce_username = "sap.integration@vikramsolar.com.aapdev"
# salesforce_password = "API@12345"
# salesforce_security_token = "OARAyU1T4ZS4nwTCLnvtEIC4"
# consumer_key = "3MVG9Gdzj3taRxuPxfPydk9KQO9MAFlKBZ1W3IiLs6mhZ_UE3s.e1ZyJEwbaADnu1FCkgwf9jU_5xzu9NZieQ"
# consumer_secret = "396CB85EC5387D6D91E776A725EAE6C248A28B4F3FB86B70A2B440754F740FE0"
#
#
# login_url = "https://test.salesforce.com/services/oauth2/token"
# oauth_data = {
#     'grant_type': 'password',
#     'client_id': consumer_key,
#     'client_secret': consumer_secret,
#     'username': salesforce_username,
#     'password': salesforce_password + salesforce_security_token
# }
#
#
# response = requests.post(login_url, data=oauth_data)
#
#
# print(f"Login Response Status Code: {response.status_code}")
# print(f"Login Response Content: {response.text}")
#
#
# if response.status_code == 200:
#     try:
#         # Attempt to parse JSON
#         json_response = response.json()
#         access_token = json_response.get('access_token')
#         print("Access Token:", access_token)
#
#         # Salesforce Bulk API endpoint
#         base_url = json_response.get('instance_url')
#         bulk_endpoint = f"{base_url}/services/async/58.0/job/"
#
#         # Define your leads data
#         leads = [
#             # {"FirstName": "yashtesting", "LastName": "NA", "Company":"NA", "Email":None,
#             {"FirstName": "yash111", "LastName": "vardhan11", "Company": "Test Cpmpss", "Email": "yash.doe@example.com",
#              "Phone": None},
#             {"FirstName": "POP111", "LastName": "111", "Email": "jaeden111.sith@example.com", "Phone": "2555-1211111",
#              "Company": "Test Comp 1111"},
#             {"FirstName": "GOH", "LastName": "NAV", "Email": "jae2.sith@example.com", "Phone": "3555-1212",
#              "Company": "Test Comp 3"},
#             {"FirstName": "AIN", "LastName": "NAV", "Email": "jae3.sith@example.com", "Phone": "4555-1213",
#              "Company": "Test Comp 4"}
#         ]
#
#         # Create a bulk job
#         job_data = {'object': 'Lead', 'operation': 'insert', 'contentType': 'JSON'}
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}',
#             'X-SFDC-Session': access_token  # Include the session ID in X-SFDC-Session header
#         }
#         response = requests.post(bulk_endpoint, json=job_data, headers=headers)
#
#         # Print the response content and status code for debugging
#         print(f"Bulk Job Creation Response Status Code: {response.status_code}")
#         print(f"Bulk Job Creation Response Content: {response.text}")
#
#         # Check if the request was successful
#         if response.status_code == 201:  # 201 indicates successful job creation
#             # Extract job ID from the Location header
#             job_id = response.headers.get('Location').split('/')[-1]
#
#             # Add batches to the job
#             batch_data = json.dumps(leads)  # Convert leads to JSON format
#             batch_url = f"{bulk_endpoint}{job_id}/batch"
#
#             # Corrected headers for batch creation
#             headers_batch = {
#                 'Content-Type': 'application/json; charset=UTF-8',
#                 'Authorization': f'Bearer {access_token}',
#                 'X-SFDC-Session': access_token
#             }
#             response = requests.post(batch_url, data=batch_data, headers=headers_batch)
#
#             # Print the response content and status code for debugging
#             print(f"Bulk Batch Creation Response Status Code: {response.status_code}")
#             print(f"Bulk Batch Creation Response Content: {response.text}")
#
#             if response.status_code == 201:  # 201 indicates successful batch creation
#                 # Extract batch ID from the Location header
#                 batch_id = response.headers.get('Location').split('/')[-1]
#                 print(f"Job ID: {job_id}")
#                 print(f"Batch ID: {batch_id}")
#             else:
#                 print("Failed to create bulk batch.")
#         else:
#             print("Failed to create bulk job.")
#
#     except Exception as e:
#         print(f"Error parsing JSON response: {e}")
# else:
#     print("Failed to authenticate with Salesforce.")
