# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:39:08 2021

@author: Túlio
"""

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
    return render_template('entry.html',the_title="Visie Desenvolvimento Web")

@app.route("/admitted_people")
def relation() -> "html":
    with UseDatabase(app.config["dbconfig"]) as cursor:
        
        _SQL = """SELECT id_pessoa,substring_index(nome, " ", 1),rg,cpf,DATE_FORMAT(data_nascimento,'%d/%m/%Y') AS niceDate,DATE_FORMAT(data_admissao,'%d/%m/%Y') as otherDate,funcao FROM pessoas""" 
                
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = tuple(["ID","Nome","RG","CPF","Data de Nascimento","Data de admissão","Função"])
    
    return render_template("view_sql.html",the_title="Processo visie",the_row_titles=titles,the_data=contents)

@app.route("/send",methods=["POST"])
def form() -> "html":
    with UseDatabase(app.config["dbconfig"]) as cursor:
        _SQL = """
        INSERT INTO pessoas(`nome`,`rg`,`cpf`,`data_nascimento`,`data_admissao`) VALUES
        (%s,%s,%s,%s,%s),
        """

        cursor.execute(_SQL)
app.secret_key = os.getenv("SECRET")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
