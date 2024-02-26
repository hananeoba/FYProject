from getpass import getpass

import requests


endpoint = 'http://127.0.0.1:8000/api/user/login/'
password = getpass( "Enter your password:")
data = {
    'email': 'me@company.com',
    'password': password,
    }

response = requests.post(endpoint, data=data)
print (response.content)