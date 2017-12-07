import json
import difflib
import csv
from bs4 import BeautifulSoup
import re

def remove_tags(text):
    return BeautifulSoup(text, 'html.parser').text

def remove_chars(text):
    return text.replace('\n','')

with open("class_content.json", "r") as f:
    j = json.loads(f.read())
    print len(j)
    print j[0].keys()

    delim = '|'
    delpat = re.compile('[|]')
    with open("questions.csv", "wb") as outf:
        csvout = csv.writer(outf, delimiter=delim)
        i = 0
        for post in j:
            subject = remove_chars(remove_tags(post['history'][0]['subject'])).encode('utf-8'),
            if type(subject) == tuple:
                subject = subject[0]
            content = remove_chars(remove_tags(post['history'][0]['content'])).encode('utf-8')

            if (re.search(delpat, content) is not None) or (re.search(delpat, subject) is not None):
                print "WARNING, skipped because of delimiter conflict"
                print '\t', subject, '\n', content[:128], "..."
                pass
            csvout.writerow([i,
                subject,
                content
                ])
            #if len(post['history']) > 1:
                # need to split by line to make this useful
                #print ''.join(difflib.ndiff([post['history'][0]['content']], [post['history'][1]['content']]))
                #print post['history']
            i += 1

