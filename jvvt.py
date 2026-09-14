import requests
 
url = 'https://viacep.com.br/ws/82640000/json/'
 
response = requests.get(url)
 
if response.status_code == 200:
    data = response.json()
    print(f'CEP: {data["cep"]}')    

