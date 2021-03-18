from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import datetime
import json
import jwt
import os
import secrets
import requests
import time
from boxsdk import OAuth2, Client

#Global Variables

SE_FOLDER_ID = '84417881026'  # SE定例
DOC_FOLDER_ID = '132869275246'  # 添付資料

class boxClient(object):
    # Authorize Box Client
    def authorize_box_client(self):
        print('Box Client 設定中')
        try:
            config = json.load(open('box_config.json'))
            appAuth = config["boxAppSettings"]["appAuth"]
            privateKey = appAuth["privateKey"]
            passphrase = appAuth["passphrase"]
            
            key = load_pem_private_key(
                data=privateKey.encode('utf8'),
                password=passphrase.encode('utf8'),
                backend=default_backend(),
            )
            
            AUTHENTICATE_URL = 'https://api.box.com/oauth2/token'

            claims = {
                'iss': config['boxAppSettings']['clientID'],
                'sub': '8808713318',
                'box_sub_type': 'user',
                'aud': AUTHENTICATE_URL,
                'jti': secrets.token_hex(64),
                'exp': round(time.time()) + 45
            }

            keyId = config['boxAppSettings']['appAuth']['publicKeyID']

            assertion = jwt.encode(claims, key, algorithm='RS512', headers={ 'kid': keyId })

            params = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': assertion,
                'client_id': config['boxAppSettings']['clientID'],
                'client_secret': config['boxAppSettings']['clientSecret']
            }

            response = requests.post(AUTHENTICATE_URL, params)
            access_token = response.json()['access_token']

            auth = OAuth2(
                client_id='YOUR_CLIENT_ID',
                client_secret='YOUR_CLIENT_SECRET',
                access_token= access_token,
            )
            
            client = Client(auth)
            return client
            
        except Exception as ex:
            print('ERR MSG: {}',format(ex))

    def get_latest_folder_id(self, client, root_folder_id='84417881026'):
        items = client.folder(folder_id=root_folder_id).get_items(sort='date')
        for item in items:
            print(item.name)
        return items
        

def GetAllItemsInFolder(client, folder_id):
    print('GetAllItemsInFolder: Folder {} 内のアイテムを捜索中'.format(folder_id))
    items = client.folder(folder_id=folder_id).get_items(sort='date')  # folder内のitemを全て取得
    return items
    

def GetLatestFolderID(client, folder_id):
    print('GetLatestFolderID： Folder {} 内の最新アイテムを捜索中'.format(folder_id))
    name = 0
    items = client.folder(folder_id=folder_id).get_items(sort='date')
    for item in items:
        if item.name.isdecimal() and int(item.name) > name:
            latest_folder_id = item.id
    print('GetLatestFolderID： Folder {}　内の最新アイテムID {}'.format(folder_id, latest_folder_id))
    return latest_folder_id


def GetDocmentFolder(items):
    print('GetDocmentFolder: 関連資料フォルダの情報を検索中')
    for item in items:
        print(item.name)
        if item.name == '関連資料':
            doc_folder = {
                'name': item.name,
                'id': item.id,
                'object_type': item.object_type
            }
            print('GetDocmentFolder: 関連資料フォルダID {}'.format(doc_folder['id']))
            return doc_folder
    

def CreateSubFolder(client, dest_folder_id, folder_name):
    items_in_dest_folder = GetAllItemsInFolder(client, dest_folder_id)
    for item in items_in_dest_folder:
        if item.name == folder_name:
            print('The same name folder already exists. ID： {}'.format(item.id))
            return item.id

    subfolder = client.folder(dest_folder_id).create_subfolder(folder_name)
    print('Created subfolder with ID {0}'.format(subfolder.id))
    return subfolder.id


def GetLatestItem(items):
    print('GetLatestItem: 最新のアイテムを捜索中')
    latest_folder_name = 0
    for item in items:
        if item.name.isdecimal() and int(item.name) > latest_folder_name:
            latest_item = { 
                'name': item.name,
                'id': item.id,
                'object_type': item.object_type
                } 
    print('GetLatestItem: 最新アイテム情報 name: {}, id: {}, type: {}'.format(latest_item['name'], latest_item['id'], latest_item['object_type']))
    return latest_item


def CopyFolder(client, target_folder_id, dest_folder_id, new_folder_name):
    items_in_dest_folder = GetAllItemsInFolder(client, dest_folder_id)
    for item in items_in_dest_folder:
        if item.name == new_folder_name:
            print('The same name folder already exists. ID： {}'.format(item.id))
            return item.id

    print('実行中：CopyFolder')
    folder_to_copy = client.folder(target_folder_id)
    dest_folder = client.folder(dest_folder_id)
    
    folder_copy = folder_to_copy.copy(dest_folder, name=new_folder_name)
    print('完了：CopyFolder  Folder {} has been copied into {}'.format(folder_copy.name, folder_copy.parent.name))
    
    return folder_copy.id


def GetNextThursday():
    dt = datetime.datetime.now()
    current_weekday = dt.weekday()
    target_weekday = 3  # 0:月曜日 1:火曜日 ... 6:日曜日

    if current_weekday < target_weekday:
        diff = target_weekday - current_weekday
    else:
        diff = target_weekday - current_weekday + 7
    diff_days = datetime.timedelta(days=diff)

    next_thu = dt + diff_days
    next_thu = next_thu.strftime("%Y%m%d")
    return next_thu


def CreateFolderSharedLink(client, folder_id):
    url = client.folder(folder_id).get_shared_link(access='collaborators')
    print('The file shared link URL is: {0}'.format(url))
    return url


def CreateFileSharedLink(client, file_id):
    url = client.file(file_id).get_shared_link(access='collaborators')
    print('The file shared link URL is: {0}'.format(url))
    return url



def CreateWebLink(client, folder_id):
    web_link = client.folder(folder_id).create_web_link('https://example.com','添付資料')
    print('Web Link url is {0} and its description is {1}'.format(web_link.url, web_link.description))

    return web_link.id


def GetWebLink(items):
    for item in items:
        if item.object_type == 'web_link':
            print('Web Link ID: {}'.format(item.id))
            return item.id

def GetBoxNoteId(items):
    for item in items:
        if 'SE定例' in item.name:
            print('SE定例 Boxnote ID: {}'.format(item.id))
            return item.id
        else: 
            print(item.name)


def UpdateFileName(client, file_id, name):
    updated_file = client.file(file_id).update_info({'name': '{}_SE定例.boxnote'.format(name)})
    # updated_file = client.file(file_id).update_info({'name': 'SE定例.boxnote'})
    print('Boxnote name has been updated to {}'.format(updated_file.name))
    return updated_file


def UpdateWebLink(client, web_link_id, url):
    updated_web_link = client.web_link(web_link_id=web_link_id).update_info({'url': url})
    print('Web Link has been updated to {}'.format(url))
    return updated_web_link


def main():
    print('main.py 実行中')
    client = boxClient().authorize_box_client()
    all_items_in_SE_Folder = GetAllItemsInFolder(client, SE_FOLDER_ID)  # SE定例フォルダの全アイテム取得
    latest_item_in_SE_Folder = GetLatestItem(all_items_in_SE_Folder)  # SE定例フォルダ内の最新のフォルダを取得
    latest_item_id = latest_item_in_SE_Folder['id']  # 最新フォルダIDを取得
    new_folder_name = GetNextThursday()  #　最新フォルダ名より新規作成フォルダ名を決定
    new_folder_id = CopyFolder(client, latest_item_id, SE_FOLDER_ID, new_folder_name)
    items_in_new_folder = GetAllItemsInFolder(client, new_folder_id)  # 新規作成フォルダの情報
    boxnote_id = GetBoxNoteId(items_in_new_folder)
    web_link_id = GetWebLink(items_in_new_folder)  #新規作成フォルダ内のWebLinkIDを取得 
    if not web_link_id:
        web_link_id = CreateWebLink(client, new_folder_id)
    print(web_link_id)
    UpdateFileName(client, boxnote_id, new_folder_name)
    doc_folder_id = CreateSubFolder(client, DOC_FOLDER_ID, new_folder_name)  #新しい日付用添付資料フォルダの作成
    boxnote_shared_url = CreateFileSharedLink(client, boxnote_id)
    web_link_shared_url = CreateFolderSharedLink(client, doc_folder_id)  #添付資料フォルダのShared Linkを作成
    UpdateWebLink(client, web_link_id, web_link_shared_url)
    

    return boxnote_shared_url, web_link_shared_url


if __name__ == '__main__':
    main()