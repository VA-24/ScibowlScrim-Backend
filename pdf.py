import PyPDF2
#scibowldb goes until 7694

pdfFileObj = open('Olympus_DE5.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

text = ""

for pageNum in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[pageNum]
    text += pageObj.extract_text()

pdfFileObj.close()

keywords = ['TOSS-UP', 'ANSWER', 'BONUS']
sections = {keyword: [] for keyword in keywords}

for keyword in keywords:
    temp = text.split(keyword)
    sections[keyword] = temp.pop(0)
    text = "".join(temp)

print(sections)