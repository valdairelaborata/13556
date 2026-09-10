# 1- Crie uma classe chamada ContaBancaria que represente uma conta bancária básica. A conta deve ter um número de conta, um titular da conta e um saldo. Implemente os seguintes métodos mágicos:
# __init__(self, numero, titular, saldo): O construtor que inicializa os atributos da conta.
# __str__(self): O método que retorna uma representação em string da conta no formato "Conta de [titular]: [saldo]".

# Além dos métodos mágicos, implemente também os seguintes métodos:
# depositar(self, valor): Adiciona um valor ao saldo da conta.
# sacar(self, valor): Retira um valor do saldo da conta, desde que haja saldo suficiente..


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
