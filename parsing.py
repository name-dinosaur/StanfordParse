import os
import csv
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from nltk.parse.corenlp import CoreNLPParser

# Start CoreNLP server first
parser = CoreNLPParser(url='http://localhost:9000')

pdfdirectory = r'data/'
directory = os.listdir(pdfdirectory)
N = len(directory)

dictionaries = [{} for _ in range(N)]
vocabulary = {}

def add_record(word, d):
	#print(word)
	global dictionaries
	t = dictionaries[d].get(word)
	if t is not None:
		t += 1
		dictionaries[d].update({ word: t })
	else:
		dictionaries[d].update({ word: 1 })
	global vocabulary
	v = vocabulary.get(word)
	if v is not None:
		v += 1
		vocabulary.update({ word: v })
	else:
		vocabulary.update({ word: 1 })

def extract_text(pdf_path, d):
	for page_layout in extract_pages(pdf_path):
		page_text = []
		for element in page_layout:
			if isinstance(element, LTTextContainer):
				page_text.append(element.get_text().strip())
		# Remove header and footer lines
		for chunk in page_text:
			if len(chunk) > 0:
				parse = next(parser.raw_parse(chunk))
			for item in parse.leaves():
				if 'http' not in item:
					item = item.lower()
					add_record(item, d)

print("\n--- PROCESSING DOCUMENTS ---\n")

# process each pdf
for i, pdf_file in enumerate(directory):
    print(f'Processing file {i + 1}/{N}: {pdf_file}')
    extract_text(os.path.join(pdfdirectory, pdf_file), i)

print("\n--- SAVING RESULTS TO CSV ---\n")

# create csv to store results
output_file = 'freq_counts.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # column titles
    col_titles = ['Vocabulary', 'Total Counts'] + directory
    writer.writerow(col_titles)

    # print word frequncies in sorted
    for word in sorted(vocabulary):
        row = [word, vocabulary[word]] + [dictionaries[i].get(word, 0) for i in range(N)]
        writer.writerow(row)

    # print totals to csv starting at 2nd col
    total_row = ['TOTAL'] + [sum(dic.get(word, 0) for dic in dictionaries) for word in sorted(vocabulary)] #sum acrosss all docs
    total_counts_per_doc = [sum(dic.values()) for dic in dictionaries] #sum accross each doc
    total_row[1:] = total_counts_per_doc
    writer.writerow(total_row)
