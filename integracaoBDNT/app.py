#import do flask para criação do servidor
#render_template para criar uma "ponte" com html
#request para capturar os dados digitados
from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

#"Ajuda" o Flask a localizar os caminhos dos arquivos
app = Flask(__name__)

bd_config = {
    'host':'localhost',
    'user':'root',
    'password':'@',
    'database':'cadastro'
}

#Criando a rota para acessar o arquivo HTML
@app.route('/')
def index():
    try:
        #Cria conexão com MySQL e permite adicionar comando SQL
        conectar = mysql.connector.connect(**bd_config)
        cursor = conectar.cursor(dictionary=True)

        #Seleção da tabela
        cursor.execute("SELECT CPF, PRIMEIRO_NOME, SOBRENOME, IDADE FROM cliente")
        lista_clientes = cursor.fetchall()

        cursor.close()
        conectar.close()
        return render_template('index.html', clientes=lista_clientes)
    
    except mysql.connector.Error as err:
        return f"Erro ao carregar a tabela: {err}"
    
#Cria uma rota para acessar o formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    #Bloco para armazenar os dados digiados
    cpf = request.form['cpf']
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    idade = request.form['idade']

    try:
        #verificando conexão com MySQL
        conectar = mysql.connector.connect(**bd_config)
        #Variável que permite a escrever SQL
        cursor = conectar.cursor()

        query = "INSERT INTO cliente(CPF,PRIMEIRO_NOME,SOBRENOME,IDADE) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(cpf,primeiro_nome,sobrenome,idade))

        #Atualiza as alterações e fecha as conexões
        conectar.commit()
        cursor.close()
        conectar.close()

        return f"<h3>Cliente {primeiro_nome} salvo com sucesso!</h3> <a href='/'>Voltar</a>"
    
    except mysql.connector.Error as err:
        return f"Erro ao gravar no banco: {err}"

#Cria a rota para exclusão
@app.route('/excluir/<cpf>')
def excluir(cpf):
    try:
        conectar = mysql.connector.connect(**bd_config)
        cursor = conectar.cursor()

        cursor.execute("DELETE FROM cliente WHERE CPF = %s", [cpf])

        conectar.commit()
        cursor.close()
        conectar.close()

        return redirect(url_for('index'))
    except mysql.connector.Error as err:
        return f"Erro ao excluir: {err}"
        
if __name__ == '__main__':
    app.run(debug=True)