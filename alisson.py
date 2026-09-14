import requests
 
cep = "80060265"
url = f"https://viacep.com.br/ws/{cep}/json/"
 
resposta = requests.get(url)
dados = resposta.json()
 
print("--- DADOS DO ENDEREÇO ---")
print("Rua: " + dados['logradouro'])
print("Bairro: " + dados['bairro'])
print("Cidade: " + dados['localidade'])
print("UF: " + dados['uf'])