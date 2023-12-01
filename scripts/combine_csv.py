import pandas as pd
import csv

# csv_file_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\combined.csv'
#
# header = ['category', 'tossup_type', 'tossup_question', 'tossup_answer',
#               'bonus_type', 'bonus_question', 'bonus_answer', 'parent_packet']
#
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(header)


file1_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\combined.csv'
file2_path = r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\.csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

result = pd.concat([df1, df2])
result.to_csv(r'C:\Users\va648\PycharmProjects\ScibowlScrim-Backend\csvs\combined.csv', index=False)
