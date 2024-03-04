import requests
import json
import re
import time
import sys

total = 0   
iteration = 0
urls_total = []
urls_prev = []
while len(urls_total) <= 520:
    urls = []
    while True:   
        r = requests.get(f'https://www.unb.com.bd/api/tag-news?tag_id=54&item={iteration}')
        #print(f'https://www.unb.com.bd/api/tag-news?tag_id=54&item={iteration}')
        if r.status_code != 200:
            raise EOFError
        if len(r.text) != 0:
            break
        time.sleep(2)
    text = re.split(":? ", r.text)
    for m in text:
        tmp = re.search(".*category.*", m)
        if tmp is not None:
            url = re.split("\"", tmp.string)
            #print(url)
            try:
                if (re.match("^https.*", url[0]) is not None):
                    url = url[0]
                else:
                    url = url[1]
            except:
                #print(sys.exc_info())
                #print(url)
                #print(tmp)
                sys.exit(-1)
            url = url.replace("\\", "")
            # if len(urls) == 0:
                #urls.append(url)
                #continue
            #if urls[len(urls)-1] != url:
                #urls.append(url)
            if url not in urls and url not in urls_prev:
                urls.append(url)
                
                
    total += len(urls)
    iteration += 1
    urls_prev = urls
    urls_total += urls
    print(iteration)

print(len(urls_total))

print(urls_total)

jlist = json.dumps(urls_total)

print(jlist)

out = open("urls.json", "w")

out.write(jlist)


out.close()