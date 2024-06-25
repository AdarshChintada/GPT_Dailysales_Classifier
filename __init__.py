from pymongo import MongoClient
from dotenv import load_dotenv
import os, json, requests, re


class LabelClassification:
    def __init__(self):
        load_dotenv()

        db_url = os.getenv("db_url")
        db_name = os.getenv("db_name")
        db_client = MongoClient(db_url)

        self.db = db_client[db_name]

    def to_alphanumeric(self, string:str):
        return re.sub(r"[^a-zA-Z0-9]", "", string).lower()

    def initiate(self, lineitems: list, pms: str):
        pms_mapping: list = self.get_pms_mapping(pms=pms)

        labels_linking = {}
        unclassified_lineitems = []

        if len(pms_mapping) > 0:
            for lineitem in lineitems:
                for i in pms_mapping:
                    if self.to_alphanumeric(lineitem) == self.to_alphanumeric(i["line_item"]):
                        labels_linking[lineitem] = i["label"]
                        break

                keys = labels_linking.keys()
                if lineitem not in keys:
                    unclassified_lineitems.append(lineitem)
        else:
            unclassified_lineitems = lineitems

        print(labels_linking)

        gpt_result = {}
        if len(unclassified_lineitems) > 0:
            print("Found unclassified lineitems, Sending to GPT")
            gpt_response = self.send_to_gpt(
                lineitems=unclassified_lineitems, prev_linking=pms_mapping
            )
            gpt_result: dict = self.process_data(gpt_response) if gpt_response else {}
        
            print(gpt_result)

        final_result = {**labels_linking, **gpt_result}

        return final_result

    def get_pms_mapping(self, pms):
        res = self.db["pms_mapping"].find_one({"pms": pms})
        return res["labels"] if res else []

    def send_to_gpt(self, lineitems: list, prev_linking: list):
        db_labels = list(self.db["labels"].find())

        api_key = os.getenv("OPENAI_API_KEY")
        format = '{"line_item": "label"}'
        labels = [i["Label"] for i in db_labels]
        
        # Note that still line item is not belongs to the label, then assign "unclassified" to that line item.
        prompt = f"""Given you a list of line items from Hotel PMS reports. 
                  Your job is to map each line item to the correct label or category based on the previously linked dictionary. 
                  If you find new line item, which not there in the dictionary then 
                  Predict the most suitable label from the below list of labels by understanding the previously linked line items pattern in the dictionary.
                  Do not give any explanation, only return the line items and associated labels in a json format like this : {format} 
                  Here is the labels list: {labels}.
                  Here is the line items list : {lineitems}
                  Here is the previously linked dictionary : {prev_linking}"""

        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": "gpt-3.5-turbo",  # we can change models here
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.2,
            },
        )
        status = response.status_code

        if status == 200:
            return response.json()

        print(status, response.text)
        return None

    def process_data(self, data):
        try:
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            print("Error occur at handling data", e)
        return None
