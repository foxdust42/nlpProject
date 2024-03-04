import json
import requests as r
import bs4
import csv 
import sys
import regex as re
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
    
out.writerow(["<url>", "<publish_date>", "<location>", "<title>", "<raw_html>", "<clean_text>"])

print(len(d))
 
print("\a\n")

for i in range(0, len(d)):

    #print(d[i])
    #d[i] = "https://www.unb.com.bd/category/Bangladesh/5-killed-in-tangail-road-crash/61684"
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
        print(f"No loc: {i}")
        
    tmp = soup.find("span", class_ = "icon qb-clock") 
    if tmp is not None:
        meta_publish = tmp.parent.contents[1]
    else:
        meta_publish = None
        print(f"No pub: {i}")
    #print(meta_publish)

    try:
        text_html = soup.find(class_ = "text")#.findChild("div")
    except:
        print(sys.exc_info())
        print(d[i])
        #sys.exit(-1)
        continue
    
    if text_html is None:
        print(f"Err: no text: {i}")
        continue
    
    garbage = text_html.__str__()

    
    children = text_html.findChildren(recursive=True)
    
    #print(text_html)
    #print(children)
    for child in children:
        
        #print(type(child.find("a")))
        if child.find_all("a") is not None:
            a ="".join([t for t in child.contents if type(t)==bs4.element.NavigableString])
            #print(child)
            #print(a.__str__())
            if re.match("(^(\u00A0)?[Rr]ead( [Mm]ore)?( )?(:)?.{0,5})|(^(\u00A0)?[Aa](ls|sl)o [Rr]ead( )?(:)?.{0,5})|(^$)|(^(\s)$)", a) is not None:
                #if a in ["Read more: ", "Read: ", "", "Also Read- ", "Read more:", "Also Read- ", "Read:", "Read : "]:
                #print("Hit!")
                child.decompose()
            
    #print(text_html.get_text())
    out.writerow([d[i], meta_publish, meta_location, title, garbage, text_html.text.strip()])
    print(i)
    #sys.exit(-1)

csvfile.close()

print("All is done\a\n")