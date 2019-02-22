from bson import ObjectId
import uuid
import time
import datetime


def check_answer_valid(answer):
    author = answer.get('author', '')
    question_id = answer.get('question_id', '')
    answer = answer.get('answer', '')
    if not all([author, question_id, answer]):
        return {'success': False, 'reason': 'author/question_id/answer 三个参数不完整'}
    if not ObjectId.is_valid(question_id):
        return {'success': False, 'reason': 'question_id不合法！'}
    return {'success': True}


def check_question_valid(question):
    author = question.get('author', '')
    title = question.get('title', '')
    if not all([author, title]):
        return {'success': False, 'reason': 'author/title/detail不能为空！'}
    return {'success': True}


def check_vote(vote_data):
    value = vote_data.get('value', '')
    doc_type = vote_data.get('doc_type', '')
    object_id = vote_data.get('doc_id', '')
    if value not in ['vote_up', 'vote_down']:
        return {'success': False, 'reason': 'value只能说`vote_up`或者`vote_down`！'}
    if not doc_type:
        return {'success': False, 'reason': 'for需要填写`question`或者`answer`！'}
    if not ObjectId.is_valid(object_id):
        return {'success': False, 'reason': f'{doc_type}_id不合法！'}
    return {'success': True}


def generate_session(user_id, user):
    now = datetime.datetime.now()
    expire_time = now + datetime.timedelta(days=30)
    session_data = {'user_id': user_id,
                    'user': user,
                    'expire_time': expire_time.timestamp()}
    session_id = str(uuid.uuid4())
    return session_id, session_data


def login_expire(session_data):
    expire_time = session_data['expire_time']
    if expire_time <= time.time():
        return True
    return False

