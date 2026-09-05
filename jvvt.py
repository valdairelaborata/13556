class ContaBancaria:
    def __init__(self, titular:str):
        self.__titular = titular
        self.__saldo = 0
 
    @property
    def titular(self):
        return self.__titular

    
    @titular.setter
    def titular(self, novo_titular):
        self.__titular = novo_titular
     
     
   
    @property
    def saldo(self):
        return self.__saldo
   
    def depositar(self, valor):
        self.__saldo += valor
 
    def sacar(self, valor):
        self.__saldo -= valor
 
 
joao = ContaBancaria('João')
 
joao.depositar(10)
joao.sacar(3)

joao.titular = "Ana"
 
print(joao.saldo)