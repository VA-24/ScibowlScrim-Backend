import json
import requests
import csv

base_url = 'https://scibowldb.com/api/questions/'

# header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
#           'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']
#
csv_file_path = '../compiled_questions.csv'
#
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)

for i in range(5504, 7695):
    print(i)
    str_i = str(i)
    url = base_url + str_i
    print(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        if 'question' in json_data:
            category = json_data['question']['category'].replace('\n', ' ')
            question_dict = {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '',
                                 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': 'SciBowlDB'}
            question_dict['category'] = category
            question_dict['tossup_type'] = json_data['question']['tossup_format'].replace('\n', ' ')
            question_dict['tossup_question'] = json_data['question']['tossup_question'].replace('\n', ' ')
            question_dict['tossup_answer'] = json_data['question']['tossup_answer'].replace('\n', ' ')
            question_dict['bonus_type'] = json_data['question']['bonus_format'].replace('\n', ' ')
            question_dict['bonus_question'] = json_data['question']['bonus_question'].replace('\n', ' ')
            question_dict['bonus_answer'] = json_data['question']['bonus_answer'].replace('\n', ' ')
            print(question_dict)

            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(question_dict.values())
        else:
            print(f"invalid JSON structure for question with ID {i}")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")