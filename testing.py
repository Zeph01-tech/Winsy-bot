import requests

api = 'https://onlinevideoconverter.pro/api/convert'

url = 'https://youtu.be/S7E9AZscgPQ'
data = {'url' : url}
response = requests.post(url=api, data=data).json()
print(response['mp3Converter'])