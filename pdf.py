import PyPDF2
import re
import os
import json
#scibowldb goes until 7694

def add_space_before_substring(s, sub):
    return s.replace(sub, ' ' + sub)

pdfFileObj = open('test.pdf', 'rb')

pdfReader = PyPDF2.PdfReader(pdfFileObj)

text = ''

for pageNum in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[pageNum]
    text += pageObj.extract_text()

pdfFileObj.close()
question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_body': '', 'tossup_answer': '', 'bonus_question': '', 'bonus_answer': ''} for i in range(24)}

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
            question_dict[j]['tossup_body'] = question_body

        #answer processing
        tossup_answer_and_bonus = question_parts[1].split('BONUS')
        tossup_answer = tossup_answer_and_bonus[0]
        tossup_answer = tossup_answer[2:]
        question_dict[j]['tossup_answer'] = tossup_answer

        #bonus processing
        bonus = tossup_answer_and_bonus[1]
        bonus = bonus.replace('\n', ' ')
        split_text = category_text + '- ' + question_type
        bonus = bonus.split(category_text)[1]
        bonus = bonus[2:]
        bonus = bonus.replace(question_type, '')
        bonus = re.sub(r'\[.*?\] ', '', bonus)
        bonus = re.sub(r'\[.*?\]', '', bonus)
        if bonus[0] == ' ':
            bonus = bonus[1:]
        question_dict[j]['bonus_question'] = bonus

        #bonus answer processing
        bonus_answer = question_parts[2]
        bonus_answer
        print(question_parts[2])

print(question_dict)
# with open('test.json', 'w') as json_file:
#     json.dump(question_dict, json_file)