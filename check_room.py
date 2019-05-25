#!/usr/bin/env python
# coding: utf-8
#
import sys
import time
import itchat
import requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s : %(message)s', filename='log.txt')


def is_room_bookable(house_id):
    url = 'http://www.ziroom.com/detail/info?id={house_id}&house_id={house_id}'.format(house_id=house_id)
    return get_room_status(url) == u'可预订'


def get_room_status(url):
    res = requests.get(url, headers={'User-Agent': 'Ziroom'})
    return res.json()['data']['air_part']['vanancy']['status']


def send_message(contact, house_id):
    itchat.send(u"房间可以预订了，快去看看吧", toUserName=contact['UserName'])
    itchat.send(u"http://m.ziroom.com/BJ/room?id={house_id}".format(house_id=house_id), toUserName=contact['UserName'])


def send_message_and_exit(house_id, myself, other_contact):
    send_message(myself, house_id)
    send_message(other_contact, house_id)
    sys._exit()


def main():
    itchat.auto_login(enableCmdQR=2)
    myself = itchat.search_friends()
    other_contact = itchat.search_friends(name="may")[0]
    house_id = 62264440
    while True:
        if is_room_bookable(house_id):
            logging.info("可预订！")
            send_message_and_exit(house_id, myself, other_contact)
        else:
            logging.info("监控中...")
        time.sleep(5)


if __name__ == '__main__':
    main()
