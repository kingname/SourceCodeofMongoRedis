import json
import datetime
import hashlib
import time
from urllib.parse import quote, unquote
from answer.MongoUtil import MongoUtil
from util.utils import check_answer_valid, check_question_valid, check_vote
from flask import Flask, render_template, request, redirect
from bson import ObjectId

app = Flask(__name__)
mongo = MongoUtil()


@app.route('/')
def index():
    question_list = mongo.query_question()
    return render_template('index.html', question_list=question_list)


@app.route('/question')
@app.route('/question/<question_id>')
def question_detail(question_id=None):
    if question_id:
        question_answer_dict = mongo.query_answer(question_id)
    return render_template('answer_list.html', question_answer_dict=question_answer_dict)


@app.route('/post_answer', methods=['POST'])
def post_answer():
    answer = request.json
    is_valid = check_answer_valid(answer)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    question_id = answer['question_id']
    author = answer['author']
    answer = answer['answer']
    mongo.insert_answer(question_id, answer, author, now)
    return json.dumps({'success': True})


@app.route('/post_question', methods=['POST'])
def post_question():
    question = request.json
    is_valid = check_question_valid(question)
    if not is_valid['success']:
        return json.dumps(is_valid, ensure_ascii=False)
    title = question['title']
    detail = question['detail']
    author = question['author']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mongo.insert_question(title, detail, author, now)
    return json.dumps({'success': True})


@app.route('/vote', methods=['POST'])
def vote():
    vote_data = request.json
    print(vote_data)
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
