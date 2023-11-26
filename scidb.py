import json
import requests

base_url = 'https://scibowldb.com/api/questions/'

for i in range(1, 7695):
    str_i = str(i)
    url = base_url + str_i

    response = requests.get(url)
    json_data = response.json()
    category = json_data['question']['category'].replace('\n', ' ')
    if category != 'MATH':
        question_dict = {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '',
                         'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': 'SciBowlDB'}
        question_dict['category'] = json_data['question']['category'].replace('\n', ' ')
        question_dict['tossup_type'] = json_data['question']['tossup_format'].replace('\n', ' ')
        question_dict['tossup_question'] = json_data['question']['tossup_question'].replace('\n', ' ')
        question_dict['tossup_answer'] = json_data['question']['tossup_answer'].replace('\n', ' ')
        question_dict['bonus_type'] = json_data['question']['bonus_format'].replace('\n', ' ')
        question_dict['bonus_question'] = json_data['question']['bonus_question'].replace('\n', ' ')
        question_dict['bonus_answer'] = json_data['question']['bonus_answer'].replace('\n', ' ')
    print(question_dict)