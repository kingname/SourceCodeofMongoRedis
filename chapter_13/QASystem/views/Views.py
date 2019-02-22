import json
from controller import Controller
from flask import Flask, render_template, request, make_response

app = Flask('QA_SYSTEM')


@app.route('/')
@app.route('/page/<page>')
def index(page=1):
    page = int(page)
    session_id = request.cookies.get('session')
    parameter = Controller.list_question(session_id, page)
    return render_template('index.html',
                           **parameter)


@app.route('/logout')
def logout():
    session_id = request.cookies.get('session')
    return Controller.logout(session_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        body = request.json
        response = Controller.login(body)
        return response


@app.route('/register', methods=['POST'])
def register():
    body = request.json
    response = Controller.register(body)
    return response


@app.route('/question/<question_id>')
@app.route('/question/<question_id>/page/<page>')
def question_detail(question_id=None, page=1):
    print('==========', page, '==========')
    page = int(page)
    session_id = request.cookies.get('session')
    parameter_dict = Controller.question_detail(session_id, question_id, page)
    return render_template('answer_list.html',
                           **parameter_dict)


@app.route('/post_answer', methods=['POST'])
def post_answer():
    session_id = request.cookies.get('session')
    answer = request.json
    response = Controller.post_answer(session_id, answer)
    return response


@app.route('/post_question', methods=['POST'])
def post_question():
    session_id = request.cookies.get('session')
    question = request.json
    response = Controller.post_question(session_id, question)
    return response


@app.route('/update', methods=['POST'])
def update():
    session_id = request.cookies.get('session')
    info = request.json
    response = Controller.update(session_id, info)
    return response


@app.route('/vote', methods=['POST'])
def vote():
    session_id = request.cookies.get('session')
    vote_data = request.json
    response = Controller.vote(session_id, vote_data)
    return response
