class Conta:
 
    def __init__(self, titular, saldo_inicial = 0):
        self.titular = titular
        self.saldo = saldo_inicial
 
    def depositar(self, valor):
        if valor > 0:
            self.saldo + valor
            print(f'Depósito de {valor} reais realizado')
        else:
            print('O valor do depósito não deve ser negativo')
 
    def sacar(self, valor):
        if self.saldo >= valor:
            print(f'Você conseguiu sacar {valor} reais')
        else:
            print('Seu saldo não pode ficar abaixo de zero')
   
    def extrato(self):
        print("extrato")
        print(f"Titular: {self.titular}")
        print(f"Saldo atual: R$ {self.saldo: } \n")
 


conta = Conta(titular = "jvvt", saldo_inicial = 10)
conta.extrato()
 
valor_deposito = float(input("Digite o valor para depósito: "))
conta.depositar(valor_deposito)
conta.extrato()
 
valor_saque = float(input("Digite o valor para saque: "))
conta.sacar(valor_saque)
conta.extrato()
 