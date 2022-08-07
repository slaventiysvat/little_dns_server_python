import json

blacklist_template = [
    'sasisa.com', 'vkontakte.com',
    'youtube.com', 'spaces.com'
]

to_json = {'blacklist': blacklist_template };

with open('blacklist.json', 'w') as f:
    json.dump(to_json, f)

#with open('sw_templates.json') as f:
#    print(f.read())