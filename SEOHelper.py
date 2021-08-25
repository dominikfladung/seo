from DocumentParser import DocumentParser
from PrintStyles import PrintStyles
import xml.dom.minidom
import requests
import validators

class SEOHelper:
    args = None
    
    def __init__(self, args):
        self.args = args

    def checkH1(self, parser):
        tagCounth1 = parser.getTagCount("h1")

        if tagCounth1 == 0:
            raise Exception('checkHeadings', "No H1 found")
        elif tagCounth1 != 1:
            raise Exception('checkHeadings', "More than one H1")

    def checkText2CodeRatio(self, parser):
        if parser.htmlMetaData['text_to_code_ratio'] < 0.2:
            raise Exception('checkText2CodeRatio', "TextToCode is more than 0.2")

    def validate(self, parser):
        self.checkH1(parser)
        self.checkText2CodeRatio(parser)
    
    def checkURL(self, url):
        request = requests.get(url)
        parser = DocumentParser()
        
        try: 
            if request.status_code == 200 or request.status_code == 301:
                parser.feed(str(request.content))
                self.validate(parser)
                
                print(f"{PrintStyles.OKGREEN} " + str(request.status_code) + " " + url + PrintStyles.ENDC)
                return True
            else:
                print(f"{PrintStyles.FAIL} !! " + str(request.status_code) + " " + url + " !!" + PrintStyles.ENDC)
                return False
        except Exception as e: 
            print(e)
            raise e
            return False

    def getURLsFromSitemap(self, sitemapURI):
        isSitemapURL = validators.url(sitemapURI)
        
        if isSitemapURL:
            r = requests.get(sitemapURI)
            doc = xml.dom.minidom.parseString(r.content)
        else:
            doc = xml.dom.minidom.parse(sitemapURI)
        
        nodes = doc.getElementsByTagName("url")

        return map(lambda item: item.getElementsByTagName('loc')[0].firstChild.nodeValue, nodes)

    def crawlSitemap(self, sitemapURI): 
        urls = self.getURLsFromSitemap(sitemapURI)
        okCounter = 0
        errorCounter = 0

        for url in urls:
            if self.checkURL(url):
                okCounter += 1
            else:
                errorCounter += 1

            return
        print("Von " + str(okCounter + errorCounter) + " sind " + PrintStyles.OKGREEN + str(okCounter) +  PrintStyles.ENDC + " OK und " + PrintStyles.FAIL + str(errorCounter) + PrintStyles.ENDC + " mit Fehlern")    
