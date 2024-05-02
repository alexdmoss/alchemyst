# --------------------------------------------------------------

### text only

# import pdftotree

# pdftotree.parse("descriptive_tm.pdf", html_path="out.html")

# --------------------------------------------------------------

### would not install

# import aspose.words as aw

# # Load the PDF file
# doc = aw.Document("descriptive_tm.pdf")

# # Save the document as HTML
# doc.save("Document.html")

# --------------------------------------------------------------

# did good job of descriptive_tm but very hard to parse output
# does handle images ok, embeds them, but hideous html!
# there are command switches to influence: https://github.com/coolwanglu/pdf2htmlEX/wiki/Command-Line-Options

# import subprocess
# inputFilename = "aromatic_heterocyclic.pdf"
# outputFilename = "out.html"
# subprocess.run(["pdf2htmlex", inputFilename, outputFilename])

# --------------------------------------------------------------

# did well with images but struggled with sup/sub, and there are loads of these

# import asposewordscloud
# import asposewordscloud.models.requests
# from shutil import copyfile

# # Please get your Client ID and Secret from https://dashboard.aspose.cloud.
# client_id=''
# client_secret=''

# words_api = asposewordscloud.WordsApi(client_id,client_secret)
# words_api.api_client.configuration.host='https://api.aspose.cloud'

# filename = 'aromatic_heterocyclic.pdf'
# dest_name = 'out.html'
# #Convert RTF to text
# request = asposewordscloud.models.requests.ConvertDocumentRequest(document=open(filename, 'rb'), format='html')

# result = words_api.convert_document(request)

# print(result)

# --------------------------------------------------------------

# clean, but formatting issues and fails totally on images
# good for extracting just the text - first function

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import BytesIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
    
test = convert_pdf_to_html('aromatic_heterocyclic.pdf')

print(test)

# --------------------------------------------------------------

# --------------------------------------------------------------
