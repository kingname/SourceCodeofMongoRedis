from bson import ObjectId


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
