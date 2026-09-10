class ContaBancaria:
    def __init__(self, numero, titular, saldo):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
 
    def __str__(self):
        return f"Conta de {self.titular}: {self.saldo}"
 
    def depositar(self, valor):
        self.saldo = self.saldo + valor
 
    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo = self.saldo - valor
        else:
            print("Saldo insuficiente")
 
 
conta = ContaBancaria(1234, "Tiago", 3600)
 
conta.depositar(462)
print(conta)

conta.sacar(300) 
print(conta)
