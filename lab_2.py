# 1- Crie uma classe ContaBancaria que inclui funcionalidades básicas e uma classe ContaCorrente que herda da classe base. 
# A classe derivada ContaCorrente substitui o método sacar para considerar um limite de saque além do saldo disponível. 

class ContaBancaria:
    def __init__(self, titular:str):
        self.__titular = titular
        self.__saldo = 0

    @property
    def saldo(self):
        return self.__saldo

    @property
    def titular(self):
        return self.__titular


    @titular.setter
    def titular(self, novo_titular):
         self.__titular = novo_titular


    def depositar(self, valor):
        self.__saldo += valor
 
    def sacar(self, valor):
        if valor <= self.__saldo:        
            self.__saldo -= valor
        else:
            print("Sem saldo suficiente!")


class ContaCorrente(ContaBancaria):
    def __init__(self, titular, limite):
        super().__init__(titular)
        self.depositar(limite)
        self.__limite = limite

    def sacar(self, valor):
        if valor <= self.saldo + self.limite:
            super().sacar(valor)
    
    @property
    def limite(self):
        return self.__limite - self.saldo
 


conta_corrente_01 = ContaCorrente("Cliente 01", 1000)
conta_corrente_01.depositar(500)
print(conta_corrente_01.saldo)

conta_corrente_01.sacar(600)
print(conta_corrente_01.saldo)


conta_corrente_01.sacar(1000)
print(conta_corrente_01.saldo)