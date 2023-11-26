import PyPDF2
#scibowldb goes until 7694

pdfFileObj = open('test.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

text = ''

for pageNum in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[pageNum]
    text += pageObj.extract_text()

pdfFileObj.close()
question_dict = {i: [] for i in range(1, 25)}

keywords = ['TOSS-UP', 'ANSWER:', 'BONUS']
text = text.split('TOSS-UP')
text.pop(0)

for j in range(len(text)):
    question = text[j].split('ANSWER')
    question = question[0][2:].replace('\n', ' ')

    if question[3] != 'X' and question[4] != 'X':
        question = question.split(' - ')

        category_text = ''
        category = question[0].split(' ')
        category.pop(0)
        for word in category:
            category_text += word + ' '

        if 'Short Answer' in question[1]:
            question_type = 'Short Answer '
            question_body = question[1].replace(question_type, '')
            if category != 'Math':
                print(question_body)
        else:
            question_type = 'Multiple Choice'