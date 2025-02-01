# StanfordParse

Objective:
Pull 3 PDFS from gov website using selenium and parse them to count words

--Instructions to use--

Download & install stanford parser.

Install imports
pip install pdfminer.six
pip install nltk
pip install selenium
pip install webdriver-manager

Pick 3 pdf urls from gov website.

Paste urls into pdfdownloadselenium.py

Run pdfdownloadselenium - which creates data folder and puts 3 pdfs into data folder, for me it named them 02036_01, 21019, 96001_01. 
These correspond to AGRICULTURAL LAND COMMISSION ACT, ACCESSIBLE BRITISH COLUMBIA ACT, ACCESS TO ABORTION SERVICES ACT

After pdfs downloaded run 

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
CTRL-C shuts the server down

Next run parsing.py
Which iterates through data folder reading pdfs to count words
This will create output csv freq_count.csv

Open csv and look at words counts
