enha = 1234
class Usuario:
    def __init__ (self, login:str, senha:int):
        self.login = login
        self.senha = senha
   
def requer_autenticacao(funcao):
    def validar(usuario, painel):
        if requer_autenticacao:
            print('Usúario autenticado')
            funcao(usuario, painel)
        else:
            print('Acesso negado. Usúario não identificado.')
    return validar
 
@requer_autenticacao
def abrir_painel(usuario, painel):
    print('Abriu o painel')
 
abrir_painel()