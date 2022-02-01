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
        if parser.htmlMetaData['text_to_code_ratio'] < 0.15:
            text_to_code_ratio = round(parser.htmlMetaData['text_to_code_ratio'], 2)
            raise Exception('checkText2CodeRatio', "TextToCodeRatio is " + str(text_to_code_ratio) + " and less than 0.15")

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

                if not self.args.only_errors:
                    print(f"{PrintStyles.OKGREEN} " + " " + url + PrintStyles.ENDC)
                return True
            else:
                raise Exception("HTTP Response Code is " + str(request.status_code) + " and not 200 or 301")
        except Exception as e: 
            print(f"{PrintStyles.FAIL} " + " " + url + " " + str(e) + PrintStyles.ENDC)
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

        print("Von " + str(okCounter + errorCounter) + " sind " + PrintStyles.OKGREEN + str(okCounter) +  PrintStyles.ENDC + " OK und " + PrintStyles.FAIL + str(errorCounter) + PrintStyles.ENDC + " mit Fehlern")    
