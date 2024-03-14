import requests

directory = requests.get('d=1104&cityId=345&locale=ru&xml=true')
print(directory.text)
