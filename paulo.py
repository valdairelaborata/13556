class ContaBancaria:
    def __init__(self, titular, conta):
        self.titular = titular
        self.conta = conta
        self.__saldo = 0  
 
    @property
    def saldo(self):
        return self.__saldo
 
    def depositar(self, valor):
        self.__saldo += valor
 
    # def sacar(self, valor):
    #     if valor >= Cnt_Bancaria.saldo:
    #         self.__saldo -= valor
 
class cnt_corrente:
    def __init__(self, titular, conta, saldo=0):
        super().__init__(titular, conta, saldo)
 
    def sacar(self, valor):
        # permite sacar até saldo + limite
        if valor > self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor} realizado. Saldo atual: R${self.saldo}")
 
 
Cnt_Bancaria = ContaBancaria('Isabella', '00001')
 
Cnt_Bancaria.depositar(5000)
 
print(Cnt_Bancaria.saldo)
 
Cnt_Bancaria.sacar(6500)
 
print(Cnt_Bancaria.saldo)