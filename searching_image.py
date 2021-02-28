import requests

headers = {
  "apikey": "339a68b0-778d-11eb-89b8-23821a7ac784"}

params = (
    ('q','bali'),
    ('tbm','isch'),
)

response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
print(response, response.text)


data = response.json()
first_image = data['image_results'][0]['thumbnail']
print(first_image)