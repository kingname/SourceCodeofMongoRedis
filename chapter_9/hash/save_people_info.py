import redis
import json
client = redis.Redis()

client.hset('people_info', '张小二', json.dumps({'age': 17, 'salary': 100, 'address': '北京'}))

other_people = {
    '王小三': json.dumps({'age': 20, 'salary': 9999, 'address': '四川'}),
    '张小四': json.dumps({'age': 30, 'salary': 0, 'address': '山东'}),
    '刘小五': json.dumps({'age': 24, 'salary': 24, 'address': '河北'}),
    '周小六': json.dumps({'age': 56, 'salary': 87, 'address': '香港'})
}

client.hmset('people_info', other_people)
print('添加完成')
