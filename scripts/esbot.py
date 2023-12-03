import PyPDF2
from docx2pdf import convert
import os
import csv
import json
import fitz
import re

def extract_integers(input_string):
    return [int(match) for match in re.findall(r'\b\d+\b', input_string)]

def add_space_before_substring(s, sub):
    return s.replace(sub, ' ' + sub)

def get_pdf_paths(root_folder):
    pdf_paths = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))

    return pdf_paths

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

root_folder = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\External Packets\ESBOT'

pdf_paths = get_pdf_paths(root_folder)
# pdf_paths = [pdf_paths[1]]
# csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\esbot.csv'
#
# header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
#               'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']
#
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)

for file in pdf_paths:
    try:
        print(file)
        packet_id = 'ESBOT'

        latex_text = extract_text_from_pdf(file)

        question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '', 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': f'{packet_id}'} for i in range(24)}

        keywords = ['TOSS-UP', 'ANSWER:', 'BONUS']
        text = latex_text.split('Tossup')
        text.pop(0)

        for j in range(0, len(text) - 1):
            question_parts = text[j].split('ANSWER')
            print(question_parts[-1])

            question = question_parts[0].replace('\n', '', 1).replace('\n', ' ')
            if 'Earth and Space' in question:
                question_dict[j]['category'] = 'Earth and Space'
                question = question.split('Earth and Space')
            if 'Physics' in question:
                question_dict[j]['category'] = 'Physics'
                question = question.split('Physics')
            if 'Biology' in question:
                question_dict[j]['category'] = 'Biology'
                question = question.split('Biology')
            if 'Chemistry' in question:
                question_dict[j]['category'] = 'Chemistry'
                question = question.split('Chemistry')
            if 'Math' in question:
                question_dict[j]['category'] = 'Math'
                question = question.split('Math')
            if 'Energy' in question:
                question_dict[j]['category'] = 'Energy'
                question = question.split('Energy')

            question = question[1]
            if 'Short Answer' in question:
                question_dict[j]['tossup_type'] = 'Short Answer'
                tossup_question = question.split('Short Answer: ')[1]
                question_dict[j]['tossup_question'] = tossup_question
            elif 'Multiple Choice' in question:
                question_dict[j]['tossup_type'] = 'Multiple Choice'
                tossup_question = question.split('Multiple Choice: ')[1]
                question_dict[j]['tossup_answer'] = tossup_question

            tossup_answer_and_bonus = question_parts[1].split('Bonus')

            tossup_answer = tossup_answer_and_bonus[0]
            tossup_answer = tossup_answer[2:]
            tossup_answer = re.sub(' +', ' ', tossup_answer.strip())
            question_dict[j]['tossup_answer'] = tossup_answer

            if len(tossup_answer_and_bonus) > 1:
                bonus = tossup_answer_and_bonus[1]
                bonus = bonus.replace('\n', ' ')
                if 'Short Answer' in bonus:
                    bonus_type = 'Short Answer'
                else:
                    bonus_type = 'Multiple Choice'
                question_dict[j]['bonus_type'] = bonus_type
                bonus = bonus.split(bonus_type)[1]
                bonus = re.sub(' +', ' ', bonus.strip())
                bonus = bonus[2:]
                question_dict[j]['bonus_question'] = bonus
                question_dict[j]['bonus_type'] = bonus_type
            else:
                bonus = ''
                bonus_type = ''
                question_dict[j]['bonus_question'] = bonus
                question_dict[j]['bonus_type'] = bonus_type


            bonus_answer = question_parts[-1]
            bonus_answer = bonus_answer[2:]
            bonus_answer = bonus_answer.split('\n')[0]
            bonus_answer = re.sub(' +', ' ', bonus_answer.strip())
            question_dict[j]['bonus_answer'] = bonus_answer


        keys_to_delete = [key for key, value in question_dict.items() if
                          value['bonus_question'] == '' or value['tossup_question'] == '']
        for key in keys_to_delete:
            del question_dict[key]

        #print(question_dict)

        for key in question_dict.keys():
            print(question_dict[key].values())
            values = list(question_dict[key].values())
            if values[0] != '':
                with open(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\esbot.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile, escapechar='\\')
                    csv_writer.writerow(question_dict[key].values())
    except:
        print('failed for ', file)

