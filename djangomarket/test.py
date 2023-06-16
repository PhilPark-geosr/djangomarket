import requests
# import requests

files = open('roads.jpg', 'rb')

upload = {'image': files}

# res = requests.post(' http://127.0.0.1:5000/image/', files = upload)
url = 'http://192.168.1.141:8000/inference/'
res = requests.post(url, files = upload)
print(res.json())