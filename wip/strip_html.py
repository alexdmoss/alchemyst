'''
Quick n dirty run-once script to strip html tags out of html files created by https://www.pdftohtml.net/
'''

from bs4 import BeautifulSoup
import os

html_files = []
for root, dirs, files in os.walk("./docs"):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for html_file in html_files:
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    out_file = html_file.replace('.html', '-2.html')
    with open(out_file, 'w') as f:
        f.write(soup.get_text())
