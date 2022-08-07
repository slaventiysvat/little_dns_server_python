import json

blacklist_template = [
    'sasisa.com', 'vcontacte.com',
    'youtube.com', 'spaces.com'
]

to_json = {'blacklist': blacklist_template };

with open('../black_list/blacklist.json', 'w') as f:
    json.dump(to_json, f)
