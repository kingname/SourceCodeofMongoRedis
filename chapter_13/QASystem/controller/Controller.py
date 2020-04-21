import json
import datetime
import config
from werkzeug.security import check_password_hash, generate_password_hash
from util.utils import check_answer_valid, check_question_valid, check_vote, generate_session
from util.BloomFilter import BloomFilter
from flask import make_response
from business_logic import MongoLogic, RedisLogic

bloom = BloomFilter(100000000, 0.001)
mongo_logic = MongoLogic()
redis_logic = RedisLogic()


def list_question(session_id, page=0):
    if page <= 0:
        start = 0
    else:
        start = (page - 1) * 3
    session_data = redis_logic.fetch_session(session_id)
    question_id_score_list = redis_logic.get_doc_rank_range('question', start, 2)
    question_list, total_question = mongo_logic.query_question(question_id_score_list)
    total_page = total_question // 3 + (1 if total_question % 3 > 0 else 0)
    page_list = [x for x in range(total_page)]
    result = {
        'question_list':question_list,
        'session':session_data,
        'current_page':page,
        'page_list':page_list
    }
    return result


def logout(session_id):
    session_data = redis_logic.fetch_session(session_id)
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    redis_logic.delete_session(session_id)
    return json.dumps({'success': True})


def login(body):
    user = body.get('user', '')
    password = body.get('password', '')
    if not all([user, password]):
        return json.dumps({'success': False, 'reason': '用户名和密码不能同时为空！'}, ensure_ascii=False)
    user_info = mongo_logic.get_user_info(user)
    if not user_info['success']:
        return json.dumps(user_info)
    password_hash = user_info['user_info']['password_hash']
    if not check_password_hash(password_hash, password):
        return json.dumps({'success': False, 'reason': '用户名与密码不匹配！'})
    session_id, session_data = generate_session(str(user_info['user_info']['_id']), user)
    redis_logic.save_session(session_id, session_data)
    response = make_response(json.dumps({'success': True}))
    response.set_cookie('session', value=session_id)
    return response


def register(body):
    user = body.get('user', '')
    password = body.get('password', '')
    if not all([user, password]):
        return json.dumps({'success': False, 'reason': '用户名和密码不能同时为空！'}, ensure_ascii=False)
    if bloom.check_duplicate(user):
        return json.dumps({'success': False, 'reason': '用户名已被注册！请更换'})
    bloom.set_key(user)
    password_hash = generate_password_hash(password)
    user_id = mongo_logic.save_user_info(user, password_hash)
    session_id, session_data = generate_session(user_id, user)
    redis_logic.save_session(session_id, session_data)
    response = make_response(json.dumps({'success': True}))
    response.set_cookie('session', value=session_id)
    return response


def question_detail(session_id, question_id, page):
    page = int(page)
    session_data = redis_logic.fetch_session(session_id)
    if page <= 0:
        start = 0
    else:
        start = (page - 1) * 3
    answer_id_score_list = redis_logic.get_doc_rank_range('answer', start, 2, question_id=question_id)
    question_answer_dict = mongo_logic.query_answer(question_id, answer_id_score_list)
    total_answer = question_answer_dict['answer_num']
    total_page = total_answer // 3 + (1 if total_answer % 3 > 0 else 0)
    page_list = list(range(total_page))
    if not page_list:
        page_list = [0]
    could_answer_this_question = True
    if 'user' not in session_data or redis_logic.check_user_answer_question(session_data['user'], question_id):
        could_answer_this_question = False
    session_data['could_answer_this_question'] = could_answer_this_question

    parameter_dict = {
        'question_answer_dict': question_answer_dict,
        'session': session_data,
        'current_page': page,
        'page_list': page_list}
    return parameter_dict


def post_answer(session_id, answer):
    session_data = redis_logic.fetch_session(session_id)
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    is_valid = check_answer_valid(answer)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    question_id = answer['question_id']
    if redis_logic.check_user_answer_question(session_data['user'], question_id):
        return json.dumps({'success': False, 'reason': '已经回答过这个问题，不能回答两次。'})
    author = session_data['user']
    answer = answer['answer']
    answer_id = mongo_logic.insert_answer(question_id, answer, author, now)
    redis_logic.add_answer_vote_set(question_id, answer_id)
    redis_logic.set_answer_flag(question_id, author)
    return json.dumps({'success': True})


def post_question(session_id, question):
    session_data = redis_logic.fetch_session(session_id)
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    is_valid = check_question_valid(question)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    title = question['title']
    detail = question['detail']
    author = session_data['user']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    doc_id = mongo_logic.insert_question(title, detail, author, now)
    redis_logic.add_question_vote_set(doc_id)
    return json.dumps({'success': True, 'doc_id': doc_id})


def update_question(info):
    if 'doc_id' not in info or 'title' not in info or 'text' not in info:
        return {'success': False, 'reason': '字段不全，必要字段：doc_id, title, text'}
    mongo_logic.update_question(info['doc_id'], info['title'], info['text'])
    return {'success': True}


def update_answer(info):
    if 'doc_id' not in info or 'text' not in info:
        return {'success': False, 'reason': '字段不全，必要字段：doc_id, text'}
    mongo_logic.update_answer(info['doc_id'], info['text'])
    return {'success': True}


def update(session_id, info):
    session_data = redis_logic.fetch_session(session_id)
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    update_type = info.get('update_type')
    if update_type == 'question':
        return json.dumps(update_question(info))
    elif update_type == 'answer':
        return json.dumps(update_answer(info))
    else:
        return json.dumps({'success': False, 'reason': 'update_type只能是qustion或者answer'})


def vote(session_id, vote_data):
    session_data = redis_logic.fetch_session(session_id)
    if not session_data:
        return json.dumps({'success': False, 'reason': '未登录！'})
    is_valid = check_vote(vote_data)
    if not is_valid['success']:
        return json.dumps(is_valid)
    doc_type = vote_data['doc_type']
    value = 1 if vote_data['value'] == 'vote_up' else -1
    doc_id = vote_data['doc_id']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mongo_logic.insert_vote(doc_type, doc_id, value, session_data['user'], now)
    redis_logic.increase_vote_score(doc_type,
                                    doc_id,
                                    value,
                                    question_id=vote_data['question_id'] if doc_type == 'answer' else '')
    return json.dumps({'success': True})
