
import requests
 
cep = "81710230"
url = f"https://viacep.com.br/ws/{cep}/json/"

resposta = requests.get(url)
dados = resposta.json()
 
if resposta.status_code == 200:
    dados = resposta.json()
    print("--- DADOS DO ENDEREÇO ---")
    print("Rua: " + dados['logradouro'])
    print("Bairro: " + dados['bairro'])
    print("Cidade: " + dados['localidade'])
    print("UF: " + dados['uf'])

else:
    print(f"Erro. Status code: {resposta.status_code}") 