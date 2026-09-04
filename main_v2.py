
class Carro:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.__velocidade = 0   

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

meu_carro = Carro("Toyota", "Corola")
meu_carro.acelerar(10)
meu_carro.frear(2)



print(meu_carro.nivel_combustivel)


