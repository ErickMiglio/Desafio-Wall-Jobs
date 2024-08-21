from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c@lebe220413",
    database="nunes_sports"
)

@app.route('/produtos', methods=['GET'])
def get_produtos():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    return jsonify(produtos)

@app.route('/produtos', methods=['POST'])
def add_produto():
    new_produto = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO produtos (nome, codigo, descricao, preco) VALUES (%s, %s, %s, %s)",
                   (new_produto['nome'], new_produto['codigo'], new_produto['descricao'], new_produto['preco']))
    db.commit()
    cursor.close()
    return jsonify(new_produto), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    updated_produto = request.json
    cursor = db.cursor()
    cursor.execute("UPDATE produtos SET nome=%s, codigo=%s, descricao=%s, preco=%s WHERE id=%s",
                   (updated_produto['nome'], updated_produto['codigo'], updated_produto['descricao'], updated_produto['preco'], id))
    db.commit()
    cursor.close()
    return jsonify(updated_produto)

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    return '', 204

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    preco = request.form['preco']
    cursor = db.cursor()
    cursor.execute("INSERT INTO produtos (nome, codigo, descricao, preco) VALUES (%s, %s, %s, %s)",
                   (nome, codigo, descricao, preco))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    nome = request.form['nome']
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    preco = request.form['preco']
    cursor = db.cursor()
    cursor.execute("UPDATE produtos SET nome=%s, codigo=%s, descricao=%s, preco=%s WHERE id=%s",
                   (nome, codigo, descricao, preco, id))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
