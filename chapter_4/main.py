import json
from flask import Flask, render_template, request
from your_code_here.DataBaseManager import DataBaseManager
from util.Checker import Checker

app = Flask(__name__)
manager = DataBaseManager()
checker = Checker()


@app.route('/')
def index():
    data_list = manager.query_info()
    return render_template('index.html', data_list=data_list)


@app.route('/add', methods=['POST'])
def add_info():
    info = request.json
    if not checker.check_add_fields_exists(info):
        return json.dumps({'success': False, 'reason': '字段不完整'}, ensure_ascii=False)
    fail_reason = checker.check_value_valid(info)
    if fail_reason:
        return json.dumps({'success': False, 'reason': fail_reason}, ensure_ascii=False)
    info['deleted'] = 0
    insert_result = manager.add_info(info)
    return json.dumps({'success': insert_result})


@app.route('/update', methods=['POST'])
def update_info():
    info = request.json
    if not checker.check_update_fields_exists(info):
        return json.dumps({'success': False, 'reason': '字段不完整'}, ensure_ascii=False)
    people_id = checker.transfer_people_id(info['people_id'])
    if people_id == -1:
        return json.dumps({'success': False, 'reason': 'ID必需为数字'})
    dict_tobe_updated = info['updated_info']
    fail_reason = checker.check_value_valid(dict_tobe_updated)
    if fail_reason:
        return json.dumps({'success': False, 'reason': fail_reason}, ensure_ascii=False)
    update_result = manager.update_info(people_id, dict_tobe_updated)
    return json.dumps({'success': update_result})


@app.route('/delete/<people_id>', methods=['GET'])
def delete(people_id):
    people_id = checker.transfer_people_id(people_id)
    if people_id > 0:
        delete_result = manager.del_info(people_id)
        return json.dumps({'success': delete_result})
    return json.dumps({'success': False, 'reason': 'ID必需为数字'})
