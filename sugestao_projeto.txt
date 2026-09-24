Biblioteca Virtual

Descritivo:
Uma aplicação para gerenciar o empréstimo de livros em uma biblioteca. Permite cadastrar livros, categorias e usuários, além de controlar quem pegou qual livro e quando deve devolvê-lo. 

Entidades e Relacionamentos:
Livro (id, titulo, autor, ano_publicacao, categoria_id)
Categoria (id, nome)
Usuário (id, nome, email)
Empréstimo (id, livro_id, usuario_id, data_retirada, data_devolucao, status) 

Funcionalidades:
CRUD de livros, categorias e usuários.
Registrar empréstimos e devoluções.
Consultar livros disponíveis e emprestados.
Validar regras de negócio (livro só pode ser emprestado se estiver disponível).