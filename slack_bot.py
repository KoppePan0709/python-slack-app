import datetime
import json
import locale
import sys

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


MSG_TMP_PATH = '/home/ec2-user/python-slack-app/slack_msg_template.json'
CONFIG_PATH = '/home/ec2-user/python-slack-app/slack_config.json'
TIME_STAMP_PATH = '/home/ec2-user/python-slack-app/timestamp.json'
NOTIFICATION_TMP_PATH = '/home/ec2-user/python-slack-app/slack_notification_msg_template.json'
# MSG_TMP_PATH = 'slack_msg_template.json'
# CONFIG_PATH = 'slack_config.json'
# TIME_STAMP_PATH = 'timestamp.json'
# NOTIFICATION_TMP_PATH = 'slack_notification_msg_template.json'

msg_template = json.load(open(MSG_TMP_PATH))
slack_config = json.load(open(CONFIG_PATH))
channel_id = slack_config['CHANNEL_ID_PROD']
# channel_id = slack_config['CHANNEL_ID_STG']
client = WebClient(token=slack_config['SLACK_BOT_TOKEN'])
LOG_PREFIX = 'slack_bot.py'

def get_next_thursday():
    # 翌木曜日の日付を取得
    # 実行日が木曜の場合は当日日付を返す。
    dt = datetime.datetime.now()
    current_weekday = dt.weekday()
    target_weekday = 3  # 0:月曜日 1:火曜日 ... 6:日曜日

    if current_weekday <= target_weekday:
        diff = target_weekday - current_weekday
    else:
        diff = target_weekday - current_weekday + 7
    diff_days = datetime.timedelta(days=diff)

    next_thu = dt + diff_days
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    next_thu = next_thu.strftime('%m月%d日（%a）')
    return next_thu


def main(boxnote_url, weblink_url):

    mtg_date = get_next_thursday()
    msg_template['blocks'][0]['text']['text'] = "*{} SE定例開催準備*".format(mtg_date)
    msg_template['blocks'][2]['text']['text'] = ":paper:  *会議資料*\n{}\n:paperclip2:  *添付資料置き場*:\n{}\n以下の担当者の方、共有事項がありましたら資料の更新をお願いいたします。".format(boxnote_url, weblink_url)

    try:
        response = client.chat_postMessage(channel=channel_id, blocks=msg_template['blocks'])
        
        data = {
            'ts': response['ts'],
            'boxnote_url': boxnote_url,
            'weblink_url': weblink_url
        }

        with open(TIME_STAMP_PATH, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(LOG_PREFIX, sys._getframe().f_code.co_name, 'ok = {}'.format(response['ok']), 'ts = {}'.format(response['ts']))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(LOG_PREFIX, sys._getframe().f_code.co_name, f"Got an error: {e.response['error']}")


def send_reminder():

    post_data = json.load(open(TIME_STAMP_PATH))
    mtg_date = get_next_thursday()
    msg_template['blocks'][0]['text']['text'] = "*{} SE定例開催準備【リマインド】*".format(mtg_date)
    msg_template['blocks'][2]['text']['text'] = ":paper:  *会議資料*\n{}\n:paperclip2:  *添付資料置き場*:\n{}\n以下の担当者の方、共有事項がありましたら資料の更新をお願いいたします。".format(post_data['boxnote_url'], post_data['weblink_url'])

    try:
        response = client.chat_postMessage(
            channel=channel_id,
            thread_ts=post_data['ts'],
            blocks=msg_template['blocks']
            )
        print(LOG_PREFIX, sys._getframe().f_code.co_name, 'ok = {}'.format(response['ok']))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(LOG_PREFIX, f"Got an error: {e.response['error']}")


def send_notification():
    notification_msg_template = json.load(open(NOTIFICATION_TMP_PATH))
    dt = datetime.datetime.now()
    meeting_date = dt.strftime('%dth %b %Y')
    meeting_link = "https://ibm.webex.com/ibm/j.php?MTID=m7c69294467d20a68f10b0105f71c2ea8"
    post_data = json.load(open(TIME_STAMP_PATH))
    notification_msg_template['blocks'][2]['text']['text'] = " :webex:  *<{meeting_link}|参加はこちらから>*\n :paper:  <{boxnote_url}|会議資料>\n :folder:  <{weblink_url}|添付資料>".format(meeting_link=meeting_link, boxnote_url=post_data['boxnote_url'], weblink_url=post_data['weblink_url'])
    notification_msg_template['blocks'][3]['elements'][0]['text'] = " :calendar: *{} 17:00-18:00pm*".format(meeting_date)
    
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=notification_msg_template['blocks']
            )
        print(LOG_PREFIX, sys._getframe().f_code.co_name, 'ok = {}'.format(response['ok']))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(LOG_PREFIX, sys._getframe().f_code.co_name, f"Got an error: {e.response['error']}")




if __name__ == '__main__':
    pass