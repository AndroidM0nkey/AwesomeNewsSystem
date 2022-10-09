import requests
import json
  
URL = "http://127.0.0.1:8002" #can be changed on demand 
headers = {'Content-type': 'application/json'}

if __name__ == '__main__':
    data = {
        'category': 'BUH',
        'timestampStart': 1,
        'timestampEnd': 50
    }
    r = requests.get(url = (URL + '/get_trend'), headers = headers, data = json.dumps(data))
    print(r.json())
