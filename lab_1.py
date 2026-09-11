# 1- Crie um decorador que verifica se o usuário está autenticado antes de executar uma função.

senha_correta = 1234

class Usuario:
    def __init__(self, login: str, senha: int):
        self.login = login
        self.senha = senha

    def __str__(self):
        return self.login


def requer_autenticacao(funcao):
    def autenticar(usuario, funcionalidade):        
        if usuario.senha == senha_correta:
            print(f'Usuário autenticado {usuario.login}.')
            funcao(usuario, funcionalidade)
        else:
            print(f'Acesso negado. Usuário {usuario.login} não identificado para fazer {funcionalidade}.')

    return autenticar


@requer_autenticacao
def abrir_painel(usuario, painel):
    print(f"Abrindo o painel {painel} para o usuário {usuario}.")

@requer_autenticacao
def salvar_pedido(usuario, pedido):
    print(f"Salvando pedido {pedido}.")

@requer_autenticacao
def emitir_nota_fiscal(usuario, nota):
    print(f"Emitindo nota fiscal {nota}.")


usuario_valido = Usuario("valdir", 1234)
usuario_invalido = Usuario("joao", 5678)


abrir_painel(usuario_valido, "Financeiro")

abrir_painel(usuario_invalido, "Financeiro")
salvar_pedido(usuario_valido, "Pedido 1")
emitir_nota_fiscal(usuario_invalido, "Nota 1")