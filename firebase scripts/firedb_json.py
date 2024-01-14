import json

from google.cloud import firestore

# def fetch_collection_as_dict(collection_name):
#     db = firestore.Client.from_service_account_json(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\credentials.json')
#     collection_ref = db.collection(collection_name)
#     docs = collection_ref.get()
#
#     collection_dict = {}
#     for doc in docs:
#         collection_dict[doc.id] = doc.to_dict()
#
#     return collection_dict
#
# def write_dict_to_json_file(dictionary, file_name):
#     with open(file_name, 'w') as json_file:
#         json.dump(dictionary, json_file)
#
# # Fetch Firestore data and write it into JSON file.
# collection_name = 'ScibowlScrim'
# data_dict = fetch_collection_as_dict(collection_name)
# write_dict_to_json_file(data_dict, 'scibowlscrim.json')

with open(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\firebase scripts\scibowlscrim.json', 'r') as file:
    data = json.load(file)

# most ugly code ive ever seen
dict = {'scibowldb': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'mit': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'esbot': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'prometheus': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'lost': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'lexington': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'nsba': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []},
             'sbst': {'math': [], 'physics': [], 'chemistry': [], 'biology': [], 'earth and space': [], 'energy': []}}

for key, value in data.items():
    if 'scibowldb' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['scibowldb']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['scibowldb']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['scibowldb']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['scibowldb']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['scibowldb']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['scibowldb']['energy'].append(key)
    if 'mit' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['mit']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['mit']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['mit']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['mit']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['mit']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['mit']['energy'].append(key)
    if 'esbot' in value['parent_packet'].lower():
        if str(value['bonus_answer']) != 'nan':
            print(value['bonus_answer'])
            if 'math' in value['category'].lower():
                dict['esbot']['math'].append(key)
            if 'physics' in value['category'].lower():
                dict['esbot']['physics'].append(key)
            if 'chemistry' in value['category'].lower():
                dict['esbot']['chemistry'].append(key)
            if 'biology' in value['category'].lower():
                dict['esbot']['biology'].append(key)
            if 'earth and space' in value['category'].lower():
                dict['esbot']['earth and space'].append(key)
            if 'energy' in value['category'].lower():
                dict['esbot']['energy'].append(key)
    if 'prometheus' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['prometheus']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['prometheus']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['prometheus']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['prometheus']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['prometheus']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['prometheus']['energy'].append(key)
    if 'lost' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['lost']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['lost']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['lost']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['lost']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['lost']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['lost']['energy'].append(key)
    if 'lexington' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['lexington']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['lexington']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['lexington']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['lexington']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['lexington']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['lexington']['energy'].append(key)
    if 'nsba' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['nsba']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['nsba']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['nsba']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['nsba']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['nsba']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['nsba']['energy'].append(key)
    if 'sbst' in value['parent_packet'].lower():
        if 'math' in value['category'].lower():
            dict['sbst']['math'].append(key)
        if 'physics' in value['category'].lower():
            dict['sbst']['physics'].append(key)
        if 'chemistry' in value['category'].lower():
            dict['sbst']['chemistry'].append(key)
        if 'biology' in value['category'].lower():
            dict['sbst']['biology'].append(key)
        if 'earth and space' in value['category'].lower():
            dict['sbst']['earth and space'].append(key)
        if 'energy' in value['category'].lower():
            dict['sbst']['energy'].append(key)

print(dict)
with open('ScibowlScrimKeys.json', 'w') as json_file:
    json.dump(dict, json_file)
