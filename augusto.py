class Conta_Bancaria:
    def __init__(self, titular, saldo_inicial=0.0):
        self.titular = titular
        self.saldo = saldo_inicial
 
    def __str__(self):
        return f"Conta de {self.titular}: {self.saldo}"
 
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return f"Depósito de R$ {valor:.2f} realizado com sucesso!"
 
    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return f"Saque de R$ {valor:.2f} realizado com sucesso!"
        else:
            return "Saque não realizado. Saldo insuficiente!"
   
    def exibir_extrato(self):
        print("--- Extrato ---")
        print(f"Titular: {self.titular}")
        print(f"Saldo atual: R$ {self.saldo:.2f}\n")
 
 
conta = Conta_Bancaria("Felipe", 100.0)
conta.exibir_extrato()
 
conta.depositar(50)
conta.exibir_extrato()
 
print(conta.sacar(140))
conta.exibir_extrato()
 
print(conta)