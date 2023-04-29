import requests
from collections.abc import Mapping

url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

data = {'file': open('F:\test\invoice1.png', 'rb'), 'modelId': ('', 'e1c8d163-c4e4-4b2a-9b00-1e7355b31138')}

response = requests.post(url, auth= requests.auth.HTTPBasicAuth('47b4c4d8-d841-11ed-8d4f-ca113ec846da', ''), files=data)

print(response.text)
