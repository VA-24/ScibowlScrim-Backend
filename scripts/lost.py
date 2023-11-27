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

root_folder = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\External Packets\LOST'

pdf_paths = get_pdf_paths(root_folder)
pdf_paths = [path for path in pdf_paths if 'Visual' not in path]
print(pdf_paths)
csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\lost.csv'

header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
              'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)

for file in pdf_paths:
    try:
        packet_id = 'LOST'

        latex_text = extract_text_from_pdf(file)


        question_dict = {i: {'category': '', 'tossup_type': '', 'tossup_question': '', 'tossup_answer': '', 'bonus_type': '', 'bonus_question': '', 'bonus_answer': '', 'parent_packet': f'{packet_id}'} for i in range(24)}

        keywords = ['TOSS-UP', 'ANSWER:', 'BONUS']
        text = latex_text.split('TOSS-UP')
        text.pop(0)

        for j in range(0, len(text) - 1):
            question_parts = text[j].split('ANSWER')
            question = question_parts[0].replace('\n', '', 1).replace('\n', ' ')

            if 'EARTH AND SPACE' in question:
                question_dict[j]['category'] = 'Earth and Space'
                question = question.split('EARTH AND SPACE')
            if 'PHYSICS' in question:
                question_dict[j]['category'] = 'Physics'
                question = question.split('PHYSICS')
            if 'BIOLOGY' in question:
                question_dict[j]['category'] = 'Biology'
                question = question.split('BIOLOGY')
            if 'CHEMISTRY' in question:
                question_dict[j]['category'] = 'Chemistry'
                question = question.split('CHEMISTRY')
            if 'MATH' in question:
                question_dict[j]['category'] = 'Math'
                question = question.split(' MATH')
            if 'ENERGY' in question:
                question_dict[j]['category'] = 'Energy'
                question = question.split('ENERGY')

            question = question[1].replace('\u200b', '')

            if 'Short Answer' in question:
                question_dict[j]['tossup_type'] = 'Short Answer'
                tossup_question = question.split('Short Answer ')[1]
                tossup_question = re.sub(r'\[.*?\] ', '', tossup_question)
                tossup_question = re.sub(r'\[.*?\]', '', tossup_question)
                tossup_question = re.sub(' +', ' ', tossup_question.strip())
                copyright_start = [match.start() for match in re.finditer(re.escape('©'), tossup_question)]
                copyright_end = [match.start() for match in re.finditer(re.escape(')'), tossup_question)]
                diff = 10000
                if len(copyright_start) > 0:
                    for par in copyright_end:
                        if par - copyright_start[0] > 0 and par - copyright_start[0] < diff:
                            diff = par - copyright_start[0]
                    tossup_question = tossup_question[:copyright_start[0]] + tossup_question[(copyright_start[0] + diff + 8):]
                    question_dict[j]['tossup_question'] = tossup_question
                    #print(tossup_question)
                else:
                    question_dict[j]['tossup_question'] = tossup_question
                    #print(tossup_question)
            elif 'Multiple Choice' in question:
                question_dict[j]['tossup_type'] = 'Multiple Choice'
                tossup_question = question.split('Multiple Choice ')[1]
                tossup_question = re.sub(r'\[.*?\] ', '', tossup_question)
                tossup_question = re.sub(r'\[.*?\]', '', tossup_question)
                tossup_question = re.sub(' +', ' ', tossup_question.strip())
                copyright_start = [match.start() for match in re.finditer(re.escape('©'), tossup_question)]
                copyright_end = [match.start() for match in re.finditer(re.escape(')'), tossup_question)]
                diff = 10000
                if len(copyright_start) > 0:
                    for par in copyright_end:
                        if par - copyright_start[0] > 0 and par - copyright_start[0] < diff:
                            diff = par - copyright_start[0]
                    tossup_question = tossup_question[:copyright_start[0]] + tossup_question[
                                                                             (copyright_start[0] + diff + 8):]
                    question_dict[j]['tossup_question'] = tossup_question
                    #print(tossup_question)
                else:
                    question_dict[j]['tossup_question'] = tossup_question
                    #print(tossup_question)

            tossup_answer_and_bonus = question_parts[1].split('BONUS')
            tossup_answer = tossup_answer_and_bonus[0]
            tossup_answer = tossup_answer.replace('\n', '')
            tossup_answer = tossup_answer[2:]
            copyright_start = [match.start() for match in re.finditer(re.escape('©'), tossup_answer)]
            copyright_end = [match.start() for match in re.finditer(re.escape(')'), tossup_answer)]
            diff = 10000
            if len(copyright_start) > 0:
                for par in copyright_end:
                    if par - copyright_start[0] > 0 and par - copyright_start[0] < diff:
                        diff = par - copyright_start[0]
                tossup_answer = tossup_answer[:copyright_start[0]] + tossup_answer[(copyright_start[0] + diff + 8):].split('   ')[0]
                question_dict[j]['tossup_answer'] = tossup_answer
            else:
                question_dict[j]['tossup_answer'] = tossup_answer


            bonus = tossup_answer_and_bonus[1]
            bonus = bonus.replace('\n', ' ')
            if 'Short Answer' in bonus:
                bonus_type = 'Short Answer'
            else:
                bonus_type = 'Multiple Choice'
            question_dict[j]['bonus_type'] = bonus_type

            bonus = bonus.split(bonus_type)[1]
            bonus = bonus.replace('\u200b', '')
            bonus = re.sub(r'\[.*?\] ', '', bonus)
            bonus = re.sub(r'\[.*?\]', '', bonus)
            bonus = re.sub(' +', ' ', bonus.strip())
            copyright_start = [match.start() for match in re.finditer(re.escape('©'), bonus)]
            copyright_end = [match.start() for match in re.finditer(re.escape(')'), bonus)]
            diff = 10000
            if len(copyright_start) > 0:
                for par in copyright_end:
                    if par - copyright_start[0] > 0 and par - copyright_start[0] < diff:
                        diff = par - copyright_start[0]
                bonus = bonus[:copyright_start[0]] + bonus[(copyright_start[0] + diff + 8):]
                question_dict[j]['bonus_question'] = bonus
            else:
                question_dict[j]['bonus_question'] = bonus


            bonus_answer = question_parts[2][2:].replace('\n', ' ')
            if '©' in bonus_answer:
                bonus_answer = bonus_answer.split('©')[0]
            bonus_answer = re.sub(' +', ' ', bonus_answer.strip())
            question_dict[j]['bonus_answer'] = bonus_answer

        for key in question_dict.keys():
            values = list(question_dict[key].values())
            if values[0] != '':
                with open(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\lost.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile, escapechar='\\')
                    csv_writer.writerow(question_dict[key].values())
    except:
        print('failed for ', file)
