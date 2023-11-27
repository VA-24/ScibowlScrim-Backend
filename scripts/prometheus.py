import PyPDF2
import re
from docx2pdf import convert
import os
import csv
import json
import fitz

def add_space_before_substring(s, sub):
    return s.replace(sub, ' ' + sub)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

def get_pdf_paths(root_folder):
    pdf_paths = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))

    return pdf_paths

base = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\External Packets\Prometheus'
pdf_paths = get_pdf_paths(base)

csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\prometheus.csv'

header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
              'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)

for file in pdf_paths:
    path = base + '/' + file
    packet_id = file[80:-4].replace('_', ' ')

    latex_text = extract_text_from_pdf(file)
    text = latex_text.split('TOSS-UP')
    text.pop(0)

    question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '', 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': f'{packet_id}'} for i in range(24)}

    for j in range(len(text)):
        question_parts = text[j].split('ANSWER')
        question = question_parts[0].replace('\n', '', 1).replace('\n', ' ')

        if question[3] != 'X' and question[4] != 'X':
            #question body processing
            question = question.split(' - ')

            category_text = ''
            category = question[0].split(' ')
            category.pop(0)
            for word in category:
                category_text += word + ' '
            category_text = category_text[:-1]
            question_dict[j]['category'] = category_text

            if 'Short Answer' in question[1]:
                question_type = 'Short Answer'
                question_dict[j]['tossup_type'] = question_type
                question_body = question[1].replace(question_type, '')
                question_body = re.sub(r'\[.*?\] ', '', question_body)
                question_body = re.sub(r'\[.*?\]', '', question_body)
                question_body = question_body[1:]
                question_dict[j]['tossup_question'] = question_body
            elif 'Multiple Choice' in question[1]:
                question_type = 'Multiple Choice'
                question_dict[j]['tossup_type'] = question_type
                question_body = question[1].replace(question_type, '')
                choices = ['W) ', 'X) ', 'Y) ', 'Z) ']
                s = question_body
                for choice in choices:
                    sub = choice
                    s = add_space_before_substring(s, sub)
                question_body = re.sub(r'\[.*?\] ', '', s)
                question_body = re.sub(r'\[.*?\]', '', question_body)
                question_body = question_body[1:]
                question_dict[j]['tossup_question'] = question_body

            #answer processing
            tossup_answer_and_bonus = question_parts[1].split('BONUS')
            tossup_answer = tossup_answer_and_bonus[0]
            tossup_answer = tossup_answer.replace('\n', '')
            tossup_answer = tossup_answer[2:]
            question_dict[j]['tossup_answer'] = tossup_answer

            #bonus processing
            bonus = tossup_answer_and_bonus[1]
            bonus = bonus.replace('\n', ' ')
            if 'Short Answer' in bonus:
                bonus_category = 'Short Answer'
            else:
                bonus_category = 'Multiple Choice'
            question_dict[j]['bonus_type'] = bonus_category

            bonus = bonus.split(bonus_category)[1]
            bonus = bonus.replace(question_type, '')
            bonus = re.sub(r'\[.*?\] ', '', bonus)
            bonus = re.sub(r'\[.*?\]', '', bonus)
            if bonus[0] == ' ':
                bonus = bonus[1:]
            question_dict[j]['bonus_question'] = bonus

            #bonus answer processing
            bonus_answer = question_parts[2]
            bonus_answer = bonus_answer.replace('\n', ' ')
            bonus_answer = bonus_answer[2:]
            bonus_answer = bonus_answer.split(' PROMETHEUS')[0]
            question_dict[j]['bonus_answer'] = bonus_answer

        else:
            question_dict[j]['category'] = 'X-Risk'


    keys_to_delete = [key for key, value in question_dict.items() if value['category'] == 'X-Risk' or value['category'] == 'Math']
    for key in keys_to_delete:
        del question_dict[key]

    for key in question_dict.keys():
        print(question_dict[key].values())
        with open(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\prometheus.csv', 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(question_dict[key].values())
