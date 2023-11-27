import PyPDF2
import re
from docx2pdf import convert
import os
import csv
import json
import fitz

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

root_folder = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\External Packets\MIT'

pdf_paths = get_pdf_paths(root_folder)

csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\mit.csv'

header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
              'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)

for file in pdf_paths:

    packet_id = file.split('Packets\MIT')[1][1:]
    packet_id = packet_id.split('round')
    packet_id = packet_id[0][:-1] + ' round ' + packet_id[1].replace('.pdf', '')

    latex_text = extract_text_from_pdf(file)


    question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '', 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': f'{packet_id}'} for i in range(24)}

    keywords = ['TOSS UP', 'ANSWER:', 'BONUS']
    text = latex_text.split('TOSS UP')
    text.pop(0)

    for j in range(len(text)):
        question_parts = text[j].split('ANSWER')
        question = question_parts[0].replace('\n', '', 1).replace('\n', ' ')

        if 'EARTH AND SPACE' in question:
            question_dict[j]['category'] = 'Earth and Space'
            question = question.split('EARTH AND SPACE ')
        if 'PHYSICS' in question:
            question_dict[j]['category'] = 'Physics'
            question = question.split('PHYSICS ')
        if 'BIOLOGY' in question:
            question_dict[j]['category'] = 'Biology'
            question = question.split('BIOLOGY ')
        if 'CHEMISTRY' in question:
            question_dict[j]['category'] = 'Chemistry'
            question = question.split('CHEMISTRY ')
        if 'MATH' in question:
            question_dict[j]['category'] = 'Math'
            question = question.split(' MATH ')
        if 'ENERGY' in question:
            question_dict[j]['category'] = 'Energy'
            question = question.split('ENERGY ')

        question = question[1]

        if 'Short Answer' in question:
            question_dict[j]['tossup_type'] = 'Short Answer'
            tossup_question = question.replace('Short Answer ', '')
            tossup_question = re.sub(r'\(.*?\) ', '', tossup_question)
            tossup_question = re.sub(r'\(.*?\)', '', tossup_question)
            question_dict[j]['tossup_question'] = tossup_question
        elif 'Multiple Choice' in question:
            question_dict[j]['tossup_type'] = 'Multiple Choice'
            tossup_question = question.replace('Multiple Choice ', '')
            tossup_question = re.sub(r'\(.*?\) ', '', tossup_question)
            tossup_question = re.sub(r'\(.*?\)', '', tossup_question)
            question_dict[j]['tossup_question'] = tossup_question

        tossup_answer_and_bonus = question_parts[1].split('BONUS')
        tossup_answer = tossup_answer_and_bonus[0]
        tossup_answer = tossup_answer.replace('\n', '')
        tossup_answer = tossup_answer[2:]
        question_dict[j]['tossup_answer'] = tossup_answer

        bonus = tossup_answer_and_bonus[1]
        bonus = bonus.replace('\n', ' ')
        if 'Short Answer' in bonus:
            bonus_type = 'Short Answer'
        else:
            bonus_type = 'Multiple Choice'
        question_dict[j]['bonus_type'] = bonus_type

        bonus = bonus.split(bonus_type + ' ')[1]
        bonus = re.sub(r'\(.*?\) ', '', bonus)
        bonus = re.sub(r'\(.*?\)', '', bonus)
        question_dict[j]['bonus_question'] = bonus

        bonus_answer = question_parts[2][2:].replace('\n', ' ')
        if 'MIT Science Bowl Invitational' in bonus_answer:
            bonus_answer = bonus_answer.split(' MIT')[0]
        question_dict[j]['bonus_answer'] = bonus_answer

    for key in question_dict.keys():
        values = list(question_dict[key].values())
        if values[0] != '':
            with open(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\mit.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile, escapechar='\\')
                csv_writer.writerow(question_dict[key].values())
