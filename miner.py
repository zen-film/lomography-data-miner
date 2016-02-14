import urllib.request as urllib
import pickle
import json
import os

API_KEY = os.environ['LOMO_API_KEY']

lomo_url = 'http://api.lomography.com/v1/cameras'
response = urllib.urlopen('{0}/?api_key={1}'.format(lomo_url, API_KEY))
response = response.read().decode('utf-8')
meta_page = json.loads(response)['meta']['page']
meta_total_entries = json.loads(response)['meta']['total_entries']
meta_per_page = json.loads(response)['meta']['per_page']
cameras = json.loads(response)['cameras']


def unigue(a, b):
    return [dict(y) for y in set(tuple(x.items()) for x in a+b)]

i = 0

while i == 0:
    if meta_page <= (meta_total_entries / meta_per_page):
        meta_page = str(meta_page)
        page_on_while = urllib.urlopen('{0}/?api_key={1}&page={2}'.format(
            lomo_url, API_KEY, meta_page)).read().decode('utf-8')
        cameras = cameras + json.loads(page_on_while)['cameras']
        meta_page = int(meta_page)
        meta_page = meta_page + 1
    else:
        i = i + 1

cameras = unigue(cameras, [])

with open('dump', 'wb') as out:
    pickle.dump(cameras, out)
