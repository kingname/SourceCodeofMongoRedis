import json
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from your_code_here.MongoUtil import MongoUtil
from your_code_here.RedisUtil import RedisUtil
from util.utils import check_answer_valid, check_question_valid, check_vote, generate_session
from flask import Flask, render_template, request, make_response

app = Flask(__name__)
mongo = MongoUtil()
redis = RedisUtil()


@app.route('/')
def index():
    session_data = redis.fetch_session(request.cookies.get('session'))
    question_list = mongo.query_question()
    return render_template('index.html', question_list=question_list, session=session_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        body = request.json
        user = body.get('user', '')
        password = body.get('password', '')
        if not all([user, password]):
            return json.dumps({'success': False, 'reason': '用户名和密码不能同时为空！'}, ensure_ascii=False)
        user_info = mongo.get_user_info(user)
        if not user_info['success']:
            return json.dumps(user_info)
        password_hash = user_info['password_hash']
        if not check_password_hash(password_hash, password):
            return json.dumps({'success': False, 'reason': '用户名与密码不匹配！'})
        session_id, session_data = generate_session(str(user_info['user_info']['_id']), user)
        response = make_response(json.dumps({'success': True}))
        response.set_cookie('session', value=session_id)
        return response


@app.route('/register', methods=['POST'])
def register():
    body = request.json
    user = body.get('user', '')
    password = body.get('password', '')
    if not all([user, password]):
        return json.dumps({'success': False, 'reason': '用户名和密码不能同时为空！'}, ensure_ascii=False)
    if redis.check_user_registered(user):
        return json.dumps({'success': False, 'reason': '用户名已被注册！请更换'})
    password_hash = generate_password_hash(password)
    user_id = mongo.save_user_info(user, password_hash)
    session_id, session_data = generate_session(user_id, user)
    redis.save_session(session_id, session_data)
    response = make_response(json.dumps({'success': True}))
    response.set_cookie('session', value=session_id)
    return response


@app.route('/question/<question_id>')
def question_detail(question_id=None):
    session_data = redis.fetch_session(request.cookies.get('session'))
    question_answer_dict = mongo.query_answer(question_id)

    could_answer_this_question = True
    if 'user' not in session_data or redis.check_user_answer_question(session_data['user'], question_id):
        could_answer_this_question = False
    session_data['could_answer_this_question'] = could_answer_this_question

    return render_template('answer_list.html', question_answer_dict=question_answer_dict, session=session_data)


@app.route('/post_answer', methods=['POST'])
def post_answer():
    session_data = redis.fetch_session(request.cookies.get('session'))
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    answer = request.json
    is_valid = check_answer_valid(answer)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    question_id = answer['question_id']
    if redis.check_user_answer_question(session_data['user'], question_id):
        return json.dumps({'success': False, 'reason': '已经回答过这个问题，不能回答两次。'})
    author = session_data['user']
    answer = answer['answer']
    mongo.insert_answer(question_id, answer, author, now)
    redis.set_answer_flag(question_id, author)
    return json.dumps({'success': True})


@app.route('/post_question', methods=['POST'])
def post_question():
    session_data = redis.fetch_session(request.cookies.get('session'))
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    question = request.json
    is_valid = check_question_valid(question)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    title = question['title']
    detail = question['detail']
    author = session_data['user']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    doc_id = mongo.insert_question(title, detail, author, now)
    return json.dumps({'success': True, 'doc_id': doc_id})


def update_question(info):
    if 'doc_id' not in info or 'title' not in info or 'text' not in info:
        return {'success': False, 'reason': '字段不全，必要字段：doc_id, title, text'}
    mongo.update_question(info['doc_id'], info['title'], info['text'])
    return {'success': True}


def update_answer(info):
    if 'doc_id' not in info or 'text' not in info:
        return {'success': False, 'reason': '字段不全，必要字段：doc_id, text'}
    mongo.update_answer(info['doc_id'], info['text'])
    return {'success': True}


@app.route('/update', methods=['POST'])
def update():
    session_data = redis.fetch_session(request.cookies.get('session'))
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    info = request.json
    update_type = info.get('update_type')
    if update_type == 'question':
        return json.dumps(update_question(info))
    elif update_type == 'answer':
        return json.dumps(update_answer(info))
    else:
        return json.dumps({'success': False, 'reason': 'update_type只能是qustion或者answer'})


@app.route('/vote', methods=['POST'])
def vote():
    session_data = redis.fetch_session(request.cookies.get('session'))
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    vote_data = request.json
    is_valid = check_vote(vote_data)
    if not is_valid['success']:
        return json.dumps(is_valid)
    doc_type = vote_data['doc_type']
    value = vote_data['value']
    doc_id = vote_data['doc_id']
    if doc_type == 'question':
        mongo.vote_for_question(doc_id, value)
    else:
        mongo.vote_for_answer(doc_id, value)
    return json.dumps({'success': True})

