
import json
import requests


endurl= "http://127.0.0.1:8000/api/user/login/"
headers = {
    "Content-Type": "application/json"

}
data = {
    "user_name":"user" ,
    "password": "1234"
}
response = requests.post(endurl, headers=headers, data=json.dumps(data))


print(response.json())