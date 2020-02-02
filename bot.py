import requests
import env
from getter import get_btc
from time import sleep

token = env.token
URL = 'https://api.telegram.org/bot' + token + '/' 

global last_update_id
last_update_id = 0 

def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()

def get_message():
    data = get_updates()

    last_object = data['result'][-1]
    upd_id = last_object['update_id']

    global last_update_id
    if last_update_id != upd_id:
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']
        message = { 'chat_id': chat_id,
                    'text': message_text}
        last_update_id = upd_id
        return message
    return None



def send_message(chat_id, text = 'wait...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)



def main():

    while 1:
        answer = get_message()
        if answer != None:
            id = answer['chat_id']
            text = answer['text']

            if text == '/btc':
                send_message(id, get_btc())  
        else:
            continue
        sleep(5)



if __name__ == '__main__':
    main()