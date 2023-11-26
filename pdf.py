import PyPDF2
import re
from docx2pdf import convert
import os
import csv
import json

"""
cast
csbl
dasoni
dast
deadbird
esbot
lexsci
lost
mit
moose
mosfet
nsba
prometheus
round share
sbl
sbst
winter + summer
wsbt
"""

def add_space_before_substring(s, sub):
    return s.replace(sub, ' ' + sub)

files = os.listdir(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\External Packets\Prometheus')

pdfFileObj = open('test.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

text = ''

for pageNum in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[pageNum]
    text += pageObj.extract_text()

pdfFileObj.close()
question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '', 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': 'Prometheus'} for i in range(24)}

keywords = ['TOSS-UP', 'ANSWER:', 'BONUS']
text = text.split('TOSS-UP')
text.pop(0)

for j in range(len(text)):
    question_parts = text[j].split('ANSWER')
    question = question_parts[0].replace('\n', '')

    if question[3] != 'X' and question[4] != 'X':
        #question body processing
        question = question.split(' - ')

        category_text = ''
        category = question[0].split(' ')
        category.pop(0)
        for word in category:
            category_text += word + ' '
        #print(category_text)
        question_dict[j]['category'] = category_text

        if 'Short Answer' in question[1]:
            question_type = 'Short Answer '
            question_dict[j]['tossup_type'] = question_type
            question_body = question[1].replace(question_type, '')
            question_body = re.sub(r'\[.*?\] ', '', question_body)
            question_body = re.sub(r'\[.*?\]', '', question_body)
            question_dict[j]['tossup_body'] = question_body
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
            bonus_category = 'Short Answer '
        else:
            bonus_category = 'Multiple Choice '
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
        question_dict[j]['category'] = 'X-Risk '


keys_to_delete = [key for key, value in question_dict.items() if value['category'] == 'Math ' or value['category'] == 'X-Risk ']
for key in keys_to_delete:
    del question_dict[key]

print(question_dict)
