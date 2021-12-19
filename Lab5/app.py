from flask import Flask, render_template
from db.sqlite_db_api import DatabaseClient

app = Flask(__name__, template_folder='./templates')
db = DatabaseClient()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/technique/')
def get_all_technique():
    techniques = db.get_all_technique()
    return render_template('technique_list.html', techniques=techniques)


@app.route('/technique/<int:id>')
def get_technique_by_id(id):
    technique = db.get_technique_by_id(id)
    return render_template('technique_detail.html', technique=technique)


@app.route('/about/')
def get_contacts():
    print("Contacts VIEW")
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
