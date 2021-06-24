# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:39:08 2021

@author: Túlio
"""

from datetime import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request,escape, session, copy_current_request_context

from DBcm import UseDatabase

app = Flask(__name__)
load_dotenv()

app.config["dbconfig"] = dict(host=os.getenv("HOST"),
                              user=os.getenv("USER"),
                              password=os.getenv("PASSWORD"),
                              database=os.getenv("DATABASE")
                        )

@app.route("/")
def index() -> "html":
    with UseDatabase(app.config["dbconfig"]) as cursor:
        
        _SQL = """SELECT id_pessoa,substring_index(nome, " ", 1) as nome,rg,cpf,DATE_FORMAT(data_nascimento,'%d/%m/%Y') AS niceDate,DATE_FORMAT(data_admissao,'%d/%m/%Y') as otherDate,funcao FROM pessoas""" 
                
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = tuple(["ID","Nome","RG","CPF","Data de Nascimento","Data de admissão","Função"])
    print(contents)
    return render_template('entry.html',the_title="Visie Desenvolvimento Web",the_row_titles=titles,the_data=contents)
    
@app.route("/excluir/<id>",methods=["GET"])
def excluir(id) -> "html":

    print(id)
    @copy_current_request_context
    def id_request(req: int):

        with UseDatabase(app.config["dbconfig"]) as cursor:

            _SQL = """DELETE FROM pessoas WHERE id_pessoa=%s"""

            cursor.execute(_SQL,(req,))

    id_request(id)

    return "Dado excluido com sucesso"

@app.route("/send",methods=["POST"])
def form() -> "html":

    @copy_current_request_context
    def form_request(req: "flask_request"):
        """
        Send the form to insert in the database
        """
        with UseDatabase(app.config["dbconfig"]) as cursor:
            _SQL = """
                INSERT INTO pessoas(`nome`,`rg`,`cpf`,`data_nascimento`,`data_admissao`) VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(_SQL,(req.form["nome"],req.form["rg"],req.form["cpf"],datetime.strptime(req.form["data_nasc"],"%Y-%m-%d"),"2021-06-06",))
    
    nome = request.form["nome"]
    rg = request.form["rg"]
    cpf = request.form["cpf"]
    data_nasc = request.form["data_nasc"]

    form_request(request)

    return render_template("inserted_results.html",the_title="Visie Desenvolvimento Web",the_nome=nome,the_rg=rg,the_cpf=cpf,the_data_nasc=data_nasc)



app.secret_key = os.getenv("SECRET")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
