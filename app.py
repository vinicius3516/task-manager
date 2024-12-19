import pymysql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Conexão com o banco de dados
try:
    db = pymysql.connect(
        host="34.57.252.118",  # IP público da instância Cloud SQL
        user="root",
        password="@Vinny629233",
        database="task_manager",
        port=3306  # Porta padrão do MySQL
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
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=3306)
