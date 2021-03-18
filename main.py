import slack_bot
import box_bot

def main():
    boxnote_shared_url, web_link_shared_url = box_bot.main()
    slack_bot.main(boxnote_shared_url, web_link_shared_url)


if __name__ == '__main__':
    main()