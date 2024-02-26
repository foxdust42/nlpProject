import json
import requests as r
from html.parser import HTMLParser

class BangladeshAccidentScraper(HTMLParser):
    # the .upper-box class has a single instance and it contains tha title + some metadata 
    in_upper_box : bool = False
    in_title : bool = False
    
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
    
    def restore(self):
        self.in_upper_box = False
        self.in_title = False
    
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        #return super().handle_starttag(tag, attrs)
        # print ("Tag:", tag)
        # for attr in attrs:
        #     print ("    attr: ", attr)
        #     print(attr[0])
        # print("\n") 
        # if attrs is not None and len(attrs) >= 1:
        #     print("A::", attrs[0][0], attrs[0][1])
        if attrs is not None and len(attrs) >= 1 and attrs[0][0] == "class" and attrs[0][1] == "upper-box":
            self.in_upper_box = True
            return
        if self.in_upper_box == True and tag == "h2":
            self.in_title = True;
            return
    
    def handle_data(self, data: str) -> None:
        #return super().handle_data(data)
        if self.in_title == True:
            print("Title:", data.strip())
            self.in_title = False
            self.in_upper_box = False
            return
    

with open("urls.json", "r") as f:
    d = json.load(f)
    #print(d)
    
if d is None:
    raise IOError

print(d[0])

req = r.get(d[0])

#print(req.text)
print('Resp =', req.status_code)

parser = BangladeshAccidentScraper()

parser.feed(req.text)

