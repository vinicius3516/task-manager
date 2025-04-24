import pymysql
import os
import time
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Configurações do banco de dados
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', 3306))

# Conecta ao banco com tentativas
def connect_with_retry(retries=10, delay=3):
    for i in range(retries):
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            print("Conexão com o banco foi bem-sucedida (fase de criação)!")
            return connection
        except pymysql.MySQLError as err:
            print(f"Tentativa {i+1}/{retries} - Erro ao conectar ao banco (fase de criação): {err}")
            time.sleep(delay)
    return None

# Inicializa o banco de dados (cria se não existir)
def initialize_database():
    connection = connect_with_retry()
    if not connection:
        print("Não foi possível conectar ao banco para inicialização.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Banco de dados '{DB_NAME}' verificado/criado com sucesso.")
        connection.select_db(DB_NAME)

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
    except pymysql.MySQLError as err:
        print(f"Erro ao inicializar o banco de dados: {err}")
    finally:
        connection.close()

# Inicializa banco
initialize_database()

# Tenta conectar ao banco (de novo, agora com o DB_NAME)
def connect_app_db(retries=10, delay=3):
    for i in range(retries):
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT
            )
            print("Conexão com o banco foi bem-sucedida!")
            return conn
        except pymysql.MySQLError as err:
            print(f"Tentativa {i+1}/{retries} - Erro ao conectar ao banco: {err}")
            time.sleep(delay)
    return None

db = connect_app_db()

# Rota principal
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

# Adiciona tarefa
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

# Exclui tarefa
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

# Inicializa app Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"Executando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
