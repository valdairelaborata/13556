# 1- Considere uma classe de Conta Bancária e aplique os conceitos de encapsulamento para movimentar o saldo e a troca do titular.

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
        self.__saldo -= valor




conta_01 = ContaBancaria("Valdair")

print(f'{conta_01.titular} - {conta_01.saldo}')

conta_01.depositar(10)
conta_01.depositar(10)
conta_01.depositar(10)

conta_01.sacar(5)

conta_01.titular = "Ana"

print(f'{conta_01.titular} - {conta_01.saldo}')

