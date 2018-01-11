from pyzotero import zotero
import dropbox

#zotero collection 
collection_name = 'Unread'

storage_path = 'C:\\Users\\james\\Zotero\\storage'
dropbox_path = '/Share/Literature'

#setup zotero api
zotero_key = open('zotero.key','r+').read()
dropbox_key = open('dropbox.key','r+').read()
user_ID = 4007449
zot = zotero.Zotero(user_ID, 'user', zotero_key)

#get list of collections
collections = zot.all_collections('')

#find desired collection
for collection in collections:
    if collection['data']['name'] == collection_name:
        chosen_collection = collection
        chosen_collection_key = collection['key']
        break

#get items from collection
items = zot.collection_items(chosen_collection_key)

item_keys = []
item_filenames = []

#get relevant info for each item
for item in items:
    if item.get('links',{}).get('enclosure',{}).get('type') == 'application/pdf': #get only pdfs
        item_keys.append(item['key']) #get keys
        item_filenames.append(item['links']['enclosure']['title']) #get pdf titles

file_paths = []

#create full paths to find files locally
for key,name in zip(item_keys,item_filenames):
    file_paths.append(storage_path + '\\' + key + '\\' + name)

#prepare dropbox api
dbx = dropbox.Dropbox(dropbox_key)

#upload each file
for path,name in zip(file_paths,item_filenames):
    with open(path, 'rb') as f:
        name = name.replace(".pdf","") #remove extension to be added later
        sanitized_name = name.translate({ord(c): None for c in '.- //!@#$'}) #remove naughty chars
        dbx.files_upload(f.read(),dropbox_path + '/' + sanitized_name + '.pdf')

print("")
