import json
import requests as r
import bs4
import csv 
#from bs4 import BeautifulSoup

with open("urls.json", "r") as f:
    d = json.load(f)
    #print(d)
    
if d is None:
    raise IOError

csvfile = open('articles.csv', 'w', newline='')

if csvfile is None:
    raise IOError

out = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
    
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
    meta_location = soup.find("span", class_ = "icon fa fa-map-marker").parent.contents[1]
    meta_publish = soup.find("span", class_ = "icon qb-clock").parent.contents[1]
    #print(meta_publish)

    text_html = soup.find(class_ = "text").findChild("div")

    garbage = text_html.__str__()

    children = text_html.findChildren("p", recursive=False)

    for child in children:
        if child.find("a") is not None:
            a ="".join([t for t in child.contents if type(t)==bs4.element.NavigableString])
            if a in ["Read more: ", "Read: ", ""]:
                child.decompose()
            
    #print(text_html.get_text())
    out.writerow([d[i], meta_publish, meta_location, title, garbage, text_html.get_text()])

csvfile.close()

print("All is done\a\n")