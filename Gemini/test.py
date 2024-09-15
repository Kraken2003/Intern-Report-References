import requests
import json

url = 'http://127.0.0.1:5000/generate_response'
payload = {
    "question": "List all the necessary invoice details in this image.",
    "image_path": "C:\\Users\\Prithvi\\Desktop\\SEM 7\\INTERN REPORTS\\OLIVE GAEA\\samples\\invt1.jpg"
}


headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print('Response:', response.json())
else:
    print('Error:', response.status_code, response.text)
