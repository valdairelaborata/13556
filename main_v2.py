
class Carro(object):
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.__velocidade = 0   

    # def __del__(self):
    #     print(f'{self.marca} está sendo excluído')

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def nivel_combustivel(self):
        return self.__verificar_combustivel()

    @velocidade.setter
    def velocidade(self, valor):
        if valor >= 0:
            self.__velocidade = valor
        else:
            print("A velocidade não pode ser negativa!")
        

    def acelerar(self, valor):
        self.velocidade += valor

    def frear(self, valor):
        self.__velocidade -= valor

    def __verificar_combustivel(self):
        return "10L"

    def __eq__(self, value):
        if self.marca == value.marca:
            print("Marca é igual")
        else:
            print("Marca é diferente")

        if self.modelo == value.modelo:
            print("Modelo é igual")
        else:
            print("Modelo é diferente")

        return self.marca == value.marca and self.modelo == value.modelo


    # def __str__(self):
    #     return f'{self.marca} - {self.modelo}'



meu_carro = Carro("Toyota", "Corola")
teu_carro = Carro("Toyota", "Yaris")
carro_maria = Carro("Chevrolet", "Celta")
# del meu_carro

# sao_iguais = meu_carro == teu_carro

sao_iguais = meu_carro.marca == teu_carro.marca and meu_carro.modelo == teu_carro.modelo

meu_carro_igual_dela = teu_carro == carro_maria

print(sao_iguais)

