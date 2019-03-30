"""
Title:: Extractor
Brief:: Implementation of the extractor class to be used for extracting data from pdf files
Author:: Nicholas Hemstreet
Date:: 03/27/2019
"""


# Dependencies
import nltk

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator

# Different Layout items used for determining the "smart" layout of the page
from pdfminer.layout import LTItem
from pdfminer.layout import LTTextBox
from pdfminer.layout import LTTextLine
from pdfminer.layout import LTLine
from pdfminer.layout import LTRect
from pdfminer.layout import LTImage
from pdfminer.layout import LTFigure
from pdfminer.layout import LTChar
import html2text
from io import StringIO
import json
import re
import os
import sys

import string
import re



class PdfLine(object):

    def __init__(self,xPos,yPos):
        # Self check if this is one of us
        self.xPos_ = xPos
        self.yPos_ = yPos
        self.lineStr_ = ""

    def addChar(self,ltChar):

        if (ltChar.y0 < self.yPos_ + 3.0 and ltChar.y0 > self.yPos_ - 3.0):
            self.lineStr_ += ltChar._text
            return True
        else:
            return False
    
    def __str__(self):
        return self.lineStr_
    
    def getLine(self):
        return self.lineStr_


class HtmlExtractor(object):
    """
    """
    def __init__(self):
        """
        """
        self.h_ = html2text.HTML2Text()
        self.h_.ignore_links = True
    
    def extractToText(self,fileName, oFileName=None):
        """
        """
                
        htmlFile = open(fileName,"r")
        if (oFileName == None):
            oFileName = fileName.replace(".html",".txt")
        
        oFile = open(oFileName,"w")
        
        htmlStarted = False
        for l in htmlFile:
            if (not htmlStarted):
                if (l.find("<body>")):
                    htmlStarted = True
                    l = l.replace(l[0:l.find("<body>")],"")
            if (htmlStarted):
                oFile.write(h.handle(l))
        
        htmlFile.close()

        oFile.close()



# Extractor Class implementation
class PdfExtractor(object):
    """
    Implementation of the extractor class
    """
    def __init__(self, codec="utf-8"):
        self.rsrc_mgr_ = PDFResourceManager()
        self.codec_ = codec
    
    def extractToText(self,fileName, oFileName=None):
        """
        Extracts all the text from the specified file to the output file using pdfminer.

        Args:
            fileName: Name for the file to be extracted
            oFileName: Name for the output textfile, if none specified is the specified fileName
        """
        # Only allow processing of pdfs here
        if (fileName.find(".pdf") == -1):
            return None

        if (oFileName == None):
            oFileName = fileName.replace(".pdf",".txt")
        
        retStr = StringIO()
        device = TextConverter(self.rsrc_mgr_, retStr, codec=self.codec_, laparams=LAParams(char_margin= 20))

        fp = open(fileName,"rb")

        # Create the interpreter 
        interpreter = PDFPageInterpreter(self.rsrc_mgr_, device)

        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp,pagenos, maxpages = maxpages , password = password , caching = caching , check_extractable = True):
            interpreter.process_page(page)
        
        text = retStr.getvalue()

        oFile = open(oFileName,"w")

        oFile.writelines(text)

        # Close the file
        oFile.close()

        # Close the input pdf
        fp.close()

    def extractByElement(self,fileName , oFileName= None):
        """
        Extracts each element as it goes
        """
        # Only allow processing of pdfs here
        if (fileName.find(".pdf") == -1):
            return None

        if (oFileName == None):
            oFileName = fileName.replace(".pdf",".txt")
        
        retStr = StringIO()
        device = PDFPageAggregator(self.rsrc_mgr_)

        fp = open(fileName,"rb")

        # Create the interpreter 
        interpreter = PDFPageInterpreter(self.rsrc_mgr_, device)

        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        lines = []
        for page in PDFPage.get_pages(fp,pagenos, maxpages = maxpages , password = password , caching = caching , check_extractable = True):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:

                if(isinstance(element,LTChar)):

                    foundLine = False
                    for l in lines:
                        if (l.addChar(element)):
                            foundLine = True
                            break
                    if (not foundLine):
                        nLine = PdfLine(element.x0,element.y0)
                        lines.append(nLine)
                # Check if this is a textbox
                if(isinstance(element,LTTextBox) or isinstance(element,LTTextLine)):
                    print(str(element))
                    print(element.text())

        for l in lines:
            print(str(l))

        #text = retStr.getvalue()

        #oFile = open(oFileName,"w")

        #oFile.writelines(text)

        # Close the file
        #oFile.close()

        # Close the input pdf
        fp.close()

def getSortedFrequencies(frequencyDict):
    return sorted(frequencyDict.items(),key = lambda kv: kv[1])


if __name__ == "__main__":

    pdfExtractor = PdfExtractor()
    htmlExtractor = HtmlExtractor()
    h = html2text.HTML2Text()
    h.ignore_links = True
    dirName = sys.argv[1]
    docnames = []
    for path, subdirs, files in os.walk(dirName):
        
        for f in files:
            if (f.find(".pdf") != -1):
                #pdfExtractor.extractToText(os.path.join(path,f))
                print("Finsihed extracting data from:: " + f)
                print("Extracted to:: " + f.replace(".pdf",".txt"))
                docnames.append(os.path.join(path,f.replace(".pdf",".txt")))
            elif(f.find(".html") != -1):
                iName = os.path.join(path,f)
                
                htmlFile = open(iName,"r")
                #htmlExtractor.extractToText(htmlFile)
                
                docnames.append(iName.replace(".html",".txt"))

    # Basic frequency analysis of words
    frequency = {}
    words = []
    for d in docnames:
        document_text = open(d, 'r')
        text_string = document_text.read().lower()
        
        for mp in re.findall(r'\b[a-z]{3,}\b', text_string):
            words.append(mp)

    freq = nltk.FreqDist(words)

    for key,val in freq.items():
        print(str(key) + ":" + str(val))
    
    freq.plot(300,cumulative=False)


