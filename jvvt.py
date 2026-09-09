class ContaBancaria:

    def __init__(self, titular:str):

        self.__titular = titular

        self.__saldo = 430

   

    @property

    def saldo(self):

        return self.__saldo

   

    def depositar(self, valor):

        self.__saldo += valor

 

    def sacar(self, valor):

        self.__saldo -= valor

 

class ContaCorrente(ContaBancaria):

    def __init__(self, titular:str, limite = 500):
        super().__init__(titular)
        self.__limite = limite
 

    def sacar(self, valor):
        if valor <= self.saldo + self.__limite:
            print("Saque realizado")
        else:
            print("Saldo insuficiente")

