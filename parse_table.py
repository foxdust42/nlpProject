import os
import bs4
import regex as re

f = open("table_subdistricts.html", "r")

out = open("parsed.txt", "w")

soup = bs4.BeautifulSoup(f.read(), 'html.parser')

f.close()

split = re.split('\n', soup.text)

clean_list = list(filter(lambda a : a != '', split))

print(clean_list)

for entry in clean_list:

    if entry in ["District", "Upazila"]:
        continue
    elif re.match('^hideList.*', entry) is not None:
        out.write("######\n")
        #print(entry)
        out.write("".join([re.search("\S+(?=\h+\S+$)", entry).group(0), "\n"]))
        out.write("======\n")
    elif re.match('.*[Dd]istrict', entry) is not None:
        out.write("------\n")
        out.write("".join([entry.rsplit(' ',1 )[0], "\n"]))
        out.write("^^^^^^\n")
    else:
        out.write("".join([entry.rsplit(' ', 1)[0], "\n"]))
out.close()