import time
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

esclient = Elasticsearch(['localhost:9200'])
df = pd.read_pickle('./publication_files/publications_902.pkl')
print(df.shape[0])
string = ''
df2 = df
actions = []
for d in df2.values:
    #print(d[0])
    aus = ''
    afs = ''
    for a in d[3]:
        aus += a + ', '
    for af in d[4]:
        for a in af:
            afs += a + ', '
        afs = afs[:-2] + ';'

    action = {
        "_index": "pubs-index",
        "_type": "publications",
        "_id": d[0],
        "_source": {
            'pudmid': d[0],
            'title': d[1],
            'abstract': d[2],
            'authors': d[3],
            'affiliations': d[4],
            'url': d[5],
            'citations': d[6]
        }
    }

    actions.append(action)

helpers.bulk(esclient, actions)

start_time = time.time()

response = esclient.search(
    index='pubs-index',
    body={
        "query": {
            # "bool": {
            #     "must": [
            #         { "match": { "age": "40" } }
            #     ],
            #     "must_not": [
            #         { "match": { "state": "ID" } }
            #     ]
            # }
            "match": {"abstract": "cancer"}
        }
    }
)

# print(response['hits']['total']['value'], 'took=', response['took'])
print(response['hits']['hits'][0], 'took=', response['took'])
print('took=', time.time() - start_time)

start_time = time.time()
df = pd.read_pickle('./publication_files/publications_900.pkl')
df = df[df['abstract'].str.contains('cancer')]
print('took=', time.time() - start_time)
