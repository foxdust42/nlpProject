import json
import requests as r
import bs4
import csv 
import sys
#from bs4 import BeautifulSoup

with open("urls.json", "r") as f:
    d = json.load(f)
    #print(d)
    
if d is None:
    raise IOError

csvfile = open('articles.csv', 'w', newline='')

if csvfile is None:
    raise IOError

out = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL, strict=True)
    
out.writerow(["<url>", "<publish_date>", "<location>", "<title>", "<clean_text>"])
    
print("\a\n")

for i in range(0, len(d)):

    #print(d[i])

    req = r.get(d[i])

    #print(req.text)
    #print('Resp =', req.status_code)

    # parser = BangladeshAccidentScraper()

    # parser.feed(req.text)

    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    title = soup.h2.text
    tmp = soup.find("span", class_ = "icon fa fa-map-marker")
    if tmp is not None: 
        meta_location = tmp.parent.contents[1]
    else:
        meta_location = None
        
    tmp = soup.find("span", class_ = "icon qb-clock") 
    if tmp is not None:
        meta_publish = tmp.parent.contents[1]
    else:
        meta_publish = None
    #print(meta_publish)

    try:
        text_html = soup.find(class_ = "text").findChild("div")
    except AttributeError:
        print(sys.exc_info())
        print(d[i])
        #sys.exit(-1)
        continue

    garbage = text_html.__str__()

    children = text_html.findChildren(recursive=False)

    for child in children:
        if child.find("a") is not None:
            a ="".join([t for t in child.contents if type(t)==bs4.element.NavigableString])
            if a in ["Read more: ", "Read: ", "", "Also Read- "]:
                child.decompose()
            
    #print(text_html.get_text())
    out.writerow([d[i], meta_publish, meta_location, title, text_html.get_text()])
    print(i)

csvfile.close()

print("All is done\a\n")