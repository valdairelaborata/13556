class ContaBancaria:
    def __init__(self, titular, conta):
        self.titular = titular
        self.conta = conta
        self.__saldo = 0  
 
    @property
    def saldo(self):
        return self.__saldo
 
 
    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self.__saldo = valor
        else:
            print("O saldo não pode ficar negativo !")
       
 
    def depositar(self, valor):
        self.saldo += valor
 
    def sacar(self, valor):
        self.__saldo -= valor
 
   
Cnt_Bancaria = ContaBancaria('Isabella', '00001')
Cnt_Bancaria.depositar(5000)
 
print(Cnt_Bancaria.saldo)
 
Cnt_Bancaria.sacar(1500)
 
print(Cnt_Bancaria.saldo)