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

@app.route("/",methods=["POST"])
def main() -> "html":
    with UseDatabase(**app.config["dbconfig"]) as cursor:
        _SQL = """SELECT * FROM pessoas"""

        cursor.execute(_SQL)

    return render_template("base.html",the_title="Processo visie")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
