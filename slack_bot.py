import datetime
import json
import locale

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def authorize_box_client():
    #slack_config = json.load(open('slack_config.json'))
    slack_config = json.load(open('/home/ec2-user/python-slack-app/slack_config.json'))
    client = WebClient(token=slack_config['SLACK_BOT_TOKEN'])
    
    return client

def get_next_mtg_date():
    dt = datetime.datetime.now()
    dt_delta = datetime.timedelta(days=6)
    dt += dt_delta
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    dt = dt.strftime('%m月%d日（%a）')

    return dt


def main(boxnote_url, weblink_url):
    
    client = authorize_box_client()
    
    #msg_template = json.load(open('slack_msg_template.json'))
    msg_template = json.load(open('/home/ec2-user/python-slack-app/slack_msg_template.json'))
    #slack_config = json.load(open('slack_config.json'))
    slack_config = json.load(open('/home/ec2-user/python-slack-app/slack_config.json'))
    # channel_id = slack_config['CHANNEL_ID_PROD']
    channel_id = slack_config['CHANNEL_ID_STG']
    
    mtg_date = get_next_mtg_date()
    msg_template['blocks'][0]['text']['text'] = "*{} SE定例開催準備*".format(mtg_date)
    msg_template['blocks'][2]['text']['text'] = ":paper:  *会議資料*\n{}\n:paperclip2:  *添付資料置き場*:\n{}\n以下の担当者の方、共有事項がありましたら資料の更新をお願いいたします。".format(boxnote_url, weblink_url)

    try:
        response = client.chat_postMessage(channel=channel_id, blocks=msg_template['blocks'])
        print('ok = {}'.format(response['ok']))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    boxnote_url = 'https://example.com'
    weblink_url = 'https://example.com'
    main(boxnote_url, weblink_url)
