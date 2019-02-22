import redis
import json

client = redis.Redis(host='xxx.xxx.xx.xx')

while True:
    phone_info_bytes = client.lpop('phone_queue')
    if not phone_info_bytes:
        print('短信发送完毕！')
        break

    phone_info = json.loads(phone_info_bytes.decode())
    retry_times = phone_info.get('retry_times', 0)
    phone_number = phone_info['phone_number']
    result = send_sms(phone_number)
    if result:
        print(f'手机号：{phone_number} 短信发送成功！')
        continue

    if retry_times >= 3:
        print(f'重试超过3次，放弃手机号：{phone_number}')
        continue
    next_phone_info = {'phone_number': phone_number, 'retry_times': retry_times + 1}
    client.rpush('phone_queue', json.dumps(next_phone_info))