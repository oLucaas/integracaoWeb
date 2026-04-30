#import do flask para criação do servidor
#render_template para criar uma "ponte" com html
#request para capturar os dados digitados
from flask import Flask, render_template, request
import mysql.connector

#"Ajuda" o Flask a localizar os caminhos dos arquivos
app = Flask(__name__)

bd_config = {
    'host':'localhost',
    'user':'root',
    'password':'', #Senha do MySQL
    'database':'cadastro'
}

#Criando a rota para acessar o arquivo HTML
@app.route('/')
def index():
    return render_template('index.html')

#Criem uma rota para acessar o formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    #Bloco para armazenar os dados digiados
    cpf = request.form['cpf']
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    idade = request.form['idade']
