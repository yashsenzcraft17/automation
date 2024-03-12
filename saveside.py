import os
import requests
import json
import openai


class OPENAIBusinesscardgpt:
    def __init__(self):
        openai.api_key = "c9085fe1ee6f4f9e8bb27361673cff9f"
        # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
        openai.api_base = "https://szc-azure-openai.openai.azure.com/"
        openai.api_type = 'azure'
        openai.api_version = '2023-03-15-preview'  # this may change in the future

        # This will correspond to the custom name you chose for your deployment when you deployed a model.
        self.deployment_name = 'testgptdeployment'
        # self.pre_text = "Give your result in the format (ClassificationResult: Your answer, Description: Reason for your answer) Understand the sentence and then classify the sentence into one or more of the following categories (Validation, Decision, Task, Interaction and None of these): "
        self.pre_text = "Extract the details from the given text of a business card. Extraction result should contain Name, Address, phone number, email address, website ,designation ,company name. return the result in json format  , only selected fields to show Text:"

    def business_card_text(self, text):
        text = self.pre_text + text

        response = openai.ChatCompletion.create(
            engine="testgptdeployment",
            messages=[{"role": "system",
                       "content": "You are an AI assistant that extracts the details from business card document."},
                      {"role": "user", "content": text}],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)

        # print(len(response["choices"][0]["text"]))

        # print(response['choices'][0]['message']['content'])
        return (response['choices'][0]['message']['content'])


if __name__ == '__main__':
    Text_GPT = OPENAIBusinesscardgpt()

    list_prompt = [
        'Mariana Anderson\n\nMarketing Manager\n\n+123-456-7890\n+123-456-7890\n\nCJ\nwww.reallygreatsite.com Business\nhello@reallygreatsite.com L\n\nogo\n\n123 Anywhere St., Any City, ST\n12345\n\n \n\x0c',
        'CLAIRE MACKINTOSH ©)\nHead of Engineering Department\n—_—_ NOVATECH TECHNOLOGIES\n\nWhere ideas grow!\nBie\n\nEas (656)-8686-869\n\n(464)- 6565-1423 JQ\n\nclairem@novatechtechnologies.com\n\n425 Hidden Valley Road, NY 87903 eY\n\n \n\nFront Side\n\n©)\n\nNovatech Technologies\nWhere ideas grow!\n\nwww.novetechtechnologies.com\n\n \n\nBack Side\n\x0c',
        '\x0c']
    for prompt in list_prompt:
        print("=====================================")
        Text_GPT.business_card_text(prompt)