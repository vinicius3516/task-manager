import pymysql
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Configurações do banco de dados
DB_HOST = "104.198.7.70"
DB_USER = "root"           # Usuário do MySQL
DB_PASSWORD = "r2Q9je4eYg"  # Senha do MySQL
DB_NAME = "task_manager"   # Nome do banco de dados
DB_PORT = 3306             # Porta padrão do MySQL

# Função para criar banco de dados e tabela, caso não existam
def initialize_database():
    try:
        # Conecta ao MySQL sem especificar o banco de dados
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Cria o banco de dados, se não existir
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Banco de dados '{DB_NAME}' verificado/criado com sucesso.")

        # Conecta ao banco de dados recém-criado
        connection.select_db(DB_NAME)

        # Cria a tabela `tasks`, se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT NOT NULL AUTO_INCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATE DEFAULT NULL,
                status ENUM('Pendente', 'Concluído') DEFAULT 'Pendente',
                PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """)
        print("Tabela 'tasks' verificada/criada com sucesso.")
        connection.close()
    except pymysql.MySQLError as err:
        print(f"Erro ao inicializar o banco de dados: {err}")

# Inicializa o banco de dados
initialize_database()

# Conexão com o banco de dados
try:
    db = pymysql.connect(
        host="localhost",  # Cloud SQL Connections usa localhost
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=int(DB_PORT)
    )
    print("Conexão com o banco foi bem-sucedida!")
except pymysql.MySQLError as err:
    print(f"Erro ao conectar ao banco: {err}")
    db = None

# Rota para exibir as tarefas
@app.route('/')
def index():
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        print(f"Erro ao buscar tarefas: {e}")
        return "Erro ao buscar tarefas no banco de dados."

# Rota para adicionar uma tarefa
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)", 
                       (title, description, due_date))
        db.commit()
        return redirect('/')
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        return "Erro ao adicionar tarefa."

# Rota para excluir uma tarefa
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.commit()
        return redirect('/')
    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
        return "Erro ao excluir tarefa."

if __name__ == '__main__':
    # Obtém a porta do ambiente (padrão para Cloud Run é 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
