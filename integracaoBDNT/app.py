#Import do framework
#Import do render_template para leitura do HTML
#request para catputura dos dados
from flask import Flask, render_template, redirect, url_for, request
#biblioteca para criar conexão com mysql
import mysql.connector 

app = Flask(__name__)

#Cria conexão com o MySQL
bd_config = {
    'host':'localhost',
    'user':'root',
    'password':'@Lucas2612',
    'database':'cadastro1'
}


#Definição da rota para o index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def exibir_formulario():
    return render_template('cadastro.html')

@app.route('/clientes')
def tabela_clientes():
    try:
        conexaoIndex = mysql.connector.connect(**bd_config) 
        cursoIndex = conexaoIndex.cursor(dictionary=True)
        cursoIndex.execute("SELECT * FROM cliente1")
        #Variável que armazena os dados
        lista_clientes = cursoIndex.fetchall()

        cursoIndex.close()
        conexaoIndex.close()

        return render_template('tabela.html',clientes=lista_clientes)
        
    except mysql.connector.Error as err: 
        return f"Erro ao carregar a lista:{err}"
     
@app.route('/cadastrar', methods=['POST'])
def criar_cadastro():
    try:
        #Recebe os dados do formulário
        cpf = request.form['cpf']
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        idade = request.form['idade']

        #Criar conexão com o banco de dados
        conexao = mysql.connector.connect(**bd_config)
        
        #Levar instruções SQL do Python até o banco de dados
        curso = conexao.cursor()

        query = "INSERT INTO cliente1 (CPF, PRIMEIRO_NOME, SOBRENOME, IDADE) VALUES (%s,%s,%s,%s)"
        curso.execute(query,(cpf,primeiro_nome,sobrenome,idade))

        #salvar as alterações
        #fechar o cursor
        #fechar a conexão com o banco de dados.
        conexao.commit() #conexao
        curso.close()
        conexao.close()

        return redirect(url_for('exibir_formulario'))
    
    except mysql.connector.Error as err:
        return f"Erro ao gravar no Banco: {err}" 

@app.route('/excluir/<cpf>')
def excluir(cpf):
    try:
        conexao = mysql.connector.connect(**bd_config)
        curso = conexao.cursor()

        curso.execute("DELETE FROM cliente1 WHERE CPF = %s", (cpf,))
        conexao.commit() #conexao
        curso.close()
        conexao.close()

        return redirect(url_for('tabela_clientes'))
    except mysql.connector.Error as err:
        return f"Erro ao excluir: {err}"

if __name__ ==  '__main__':
    app.run(debug=True)


