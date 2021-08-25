from DocumentHelper import DocumentHelper
from html.parser import HTMLParser

class DocumentParser(HTMLParser):
    tagsDictionary = {}
    htmlMetaData = {}
    warnings = []
    currentTag = None
    documentHelper = DocumentHelper()

    def feed(self, html):
        self.htmlMetaData = self.documentHelper.getHTMLTextMetaData(html)
        super().feed(html)

    def handle_comment(self, data):
        self.warnings.append({"message": "Comment detected: " + data})

    def handle_starttag(self, tag, attrs):
        self.currentTag = {"name": tag, "attrs": attrs}

        if tag not in self.tagsDictionary:
            self.tagsDictionary[tag] = {}
            self.tagsDictionary[tag]['count'] = 0
            self.tagsDictionary[tag]["texts"] = []

        self.tagsDictionary[tag]['count'] += 1
    
    def handle_data(self, data):
        if self.currentTag:
            self.tagsDictionary[self.currentTag["name"]]["texts"].append(data)

    def handle_endtag(self, tag):
        self.currentTag = None

    def getTagCount(self, tag):
        return self.tagsDictionary[tag]['count'] if tag in self.tagsDictionary else 0

