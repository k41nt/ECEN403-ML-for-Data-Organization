from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import json
import re
import os


#this helper function is to remove adjacent repeated words
def remove_dup(sentence):
    sentence = sentence.split(" ")
    previous = ''
    i = 0
    while i < len(sentence):
        if sentence[i] == previous:
            sentence.remove(sentence[i])
        else:
            previous = sentence[i]
            i+=1
    sentence = " ".join(sentence)
    return sentence

#This function converts pdf to text and extracts important keywords
def convert_extract(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=LAParams(char_margin= 20))
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

    #create new txt file with same name as the pdf's
    #file_out = (path[:-3])+'.json'
    with open((path[:-3])+'json', 'w') as file_out:
        text = re.sub("\\s\\s+", "\\n", text)


        #dictionary to store the keys and values    
        dictionary = {}
        for line in text.splitlines():    
            if ": " in line:
                line = remove_dup(line).split(': ')
                print (line)
                dictionary[line[0]] = line[1]
        #now dump the dictionary into a json file
        json.dump(dictionary, file_out, sort_keys= True, indent=4)

# Main    
if __name__ == '__main__':
    #list to hold all the file names
    file_list = []

    #iterate through the path to get all pdf files
    for path, subdirs, files in os.walk(r'C:/Users/Khanh/Desktop/extraction'): # change this to current working folder
        for filename in files:
            if '.pdf' in filename:
                    file_list.append(filename)
    
    #convert and extract each file in file_list
    for file in file_list:
        convert_extract(file)
