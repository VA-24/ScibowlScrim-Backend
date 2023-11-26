import json
import requests

base_url = 'https://scibowldb.com/api/questions/'

for i in range(1, 7695):
    question_dict = {'tossup_category': '', 'tossup_type': '', 'tossup_body': ''}
    str_i = str(i)
    url = base_url + str_i

    response = requests.get(url)
    json_data = response.json()
    question_dict['tossup_category'] = json_data['question']['category']
    question_dict['tossup_type'] = json_data['question']['tossup_format']
    question_dict['tossup_body'] = json_data['question']['tossup_question']
    print(question_dict)