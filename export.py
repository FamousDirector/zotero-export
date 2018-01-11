from pyzotero import zotero
import dropbox

collection_name = 'Unread'

storage_path = 'C:\\Users\\james\\Zotero\\storage'
dropbox_path = '/Share/Literature'

zotero_key = open('zotero.key','r+').read()
dropbox_key = open('dropbox.key','r+').read()
user_ID = 4007449
zot = zotero.Zotero(user_ID, 'user', zotero_key)

collections = zot.all_collections('')
for collection in collections:
    if collection['data']['name'] == collection_name:
        chosen_collection = collection
        chosen_collection_key = collection['key']
        break

items = zot.collection_items(chosen_collection_key)

item_keys = []
item_filenames = []

for item in items:
    if item.get('links',{}).get('enclosure',{}).get('type') == 'application/pdf':
        item_keys.append(item['key'])
        item_filenames.append(item['links']['enclosure']['title'])

file_paths = []

for key,name in zip(item_keys,item_filenames):
    file_paths.append(storage_path + '\\' + key + '\\' + name)


dbx = dropbox.Dropbox(dropbox_key)

for path,name in zip(file_paths,item_filenames):
    with open(path, 'rb') as f:
        name = name.replace(".pdf","")
        sanitized_name = name.translate({ord(c): None for c in '.- //!@#$'})
        dbx.files_upload(f.read(),dropbox_path + '/' + sanitized_name + '.pdf')

print("")
