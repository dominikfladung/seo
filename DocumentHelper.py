import re

class DocumentHelper():
    cssRegex = re.compile('<style>[\s\S]+<\/style>')
    ldJsonRegex = re.compile('<script type=\"application\/ld\+json\">[\s\S]+<\/script>')
    jSRegex = re.compile('<script>[\s\S]+<\/script>')
    htmlTagRegex = re.compile('<[^>]*?>')
    
    def getHTMLTextMetaData(self, html):
        text = re.sub(self.cssRegex, '', html)
        text = re.sub(self.ldJsonRegex, '', text)
        text = re.sub(self.jSRegex, '', text)
        text = re.sub(self.htmlTagRegex, '', text)
        
        codeLen = len(html) - len(text)
        return {
            'html_len': len(html),
            'code_len': codeLen,
            'text_len': len(text),
            'word_count': len(text.split(" ")),
            'text_to_code_ratio': len(text) / codeLen,
        }
