import json
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from answer.MongoUtil import MongoUtil
from answer.RedisUtil import RedisUtil
from util.utils import check_answer_valid, check_question_valid, check_vote, generate_session
from flask import Flask, render_template, request, make_response
from util.BloomFilter import BloomFilter

app = Flask(__name__)
mongo = MongoUtil()
redis = RedisUtil()
bloom = BloomFilter(100000000, 0.001, redis)


@app.route('/')
@app.route('/page/<page>')
def index(page=0):
    page = int(page)
    session_data = redis.fetch_session(request.cookies.get('session'))
    if page <= 0:
        start = 0
    else:
        start = (page - 1) * 3
    question_id_score_list = redis.get_doc_rank_range('question', start, 2)
    question_list, total_question = mongo.query_question(question_id_score_list)
    total_page = total_question // 3 + (1 if total_question % 3 > 0 else 0)
    page_list = [x for x in range(total_page)]
    return render_template('index.html',
                           question_list=question_list,
                           session=session_data,
                           current_page=page,
                           page_list=page_list)


@app.route('/logout')
def logout():
    session_data = redis.fetch_session(request.cookies.get('session'))
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    redis.delete_session(request.cookies.get('session'))
    return json.dumps({'success': True})


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
        password_hash = user_info['user_info']['password_hash']
        if not check_password_hash(password_hash, password):
            return json.dumps({'success': False, 'reason': '用户名与密码不匹配！'})
        session_id, session_data = generate_session(str(user_info['user_info']['_id']), user)
        redis.save_session(session_id, session_data)
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
    bloom.lock(user)
    if bloom.check_duplicate(user):
        bloom.unlock(user)
        return json.dumps({'success': False, 'reason': '用户名已被注册！请更换'})
    bloom.set_key(user)
    bloom.unlock(user)
    password_hash = generate_password_hash(password)
    user_id = mongo.save_user_info(user, password_hash)
    session_id, session_data = generate_session(user_id, user)
    redis.save_session(session_id, session_data)
    response = make_response(json.dumps({'success': True}))
    response.set_cookie('session', value=session_id)
    return response


@app.route('/question/<question_id>')
@app.route('/question/<question_id>/page/<page>')
def question_detail(question_id=None, page=0):
    page = int(page)
    session_data = redis.fetch_session(request.cookies.get('session'))
    if page <= 0:
        start = 0
    else:
        start = (page - 1) * 3
    answer_id_score_list = redis.get_doc_rank_range('answer', start, 2, question_id=question_id)
    question_answer_dict = mongo.query_answer(question_id, answer_id_score_list)
    total_answer = question_answer_dict['answer_num']
    total_page = total_answer // 3 + (1 if total_answer % 3 > 0 else 0)
    print('xxxxx', total_page)
    page_list = list(range(total_page))
    could_answer_this_question = True
    if 'user' not in session_data or redis.check_user_answer_question(session_data['user'], question_id):
        could_answer_this_question = False
    session_data['could_answer_this_question'] = could_answer_this_question

    return render_template('answer_list.html',
                           question_answer_dict=question_answer_dict,
                           session=session_data,
                           current_page=page,
                           page_list=page_list)


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
    answer_id = mongo.insert_answer(question_id, answer, author, now)
    redis.add_answer_vote_set(question_id, answer_id)
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
    redis.add_question_vote_set(doc_id)
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
    value = 1 if vote_data['value'] == 'vote_up' else -1
    doc_id = vote_data['doc_id']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mongo.insert_vote(doc_type, doc_id, value, session_data['user'], now)
    redis.increase_vote_score(doc_type,
                              doc_id,
                              value,
                              question_id=vote_data['question_id'] if doc_type == 'answer' else '')
    return json.dumps({'success': True})
