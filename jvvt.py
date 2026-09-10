class ContaBancaria:
    def __init__(self, numero_conta,  titular:str):
        self.__numero_conta = numero_conta
        self.__titular = titular
        self.__saldo = 0
 
    @property
    def titular(self):
        return self.__titular
   
    @property
    def saldo(self):
        return self.__saldo
   
    def depositar(self, valor):
        self.__saldo += valor
 
    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
        else:
            print("Saldo insuficiente")
 
    @titular.setter
    def titular(self, novo_titular):
        self.__titular = novo_titular
 
    def  __str__ (self):
        return f"Conta de {self.titular}: {self.saldo}"
 
conta_bancaria = ContaBancaria('13556', 'João')
conta_bancaria.depositar(500)
print(conta_bancaria)
 
conta_bancaria.sacar(400)
print(conta_bancaria)