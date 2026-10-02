from fastapi import FastAPI
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, ConfigDict

import app



@app.get("livros/disponiveis")
def livros_disponiveis():
    livros_disponiveis = []
    livros = db.query(Livro).select(Livro.id).all()
    emprestimos = db.query(Emprestimo).where(Emprestimo.status_id == 2).all()

    for emprestimo in emprestimos:  
        if emprestimo.livro_id in livros:
            livros_indisponiveis.append(emprestimo.livro_id)





    

@app.get("livros/emprestados")
def livros_emprestados():
    livros_emprestados = []

    livros = db.query(Livro).select(Livro.id).all()
    emprestimos = db.query(Emprestimo).where(Emprestimo.status_id == 2).all()

    for emprestimo in emprestimos:  
        if emprestimo.livro_id in livros:
            livros_emprestados.append(emprestimo.livro_id)



algoritimo para listar livros disponiveis

listar todos os livros cadastrados no banco de dados
verificar se o livro está emprestado ou não
para saber se esta emprestado, verificar se o livro está na tabela de emprestimos com status 2
adiciona numa lista de livros disponiveis 


        