import pypatent
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
import json
import unicodedata


with open('authors_9.json') as json_file:
    data = json.load(json_file)

driver = webdriver.Chrome(r'C:\Users\jchaves6\PycharmProjects\Retention\chromedriver')

new_data = {}
for key in data.keys():
    print(key)
    key2 = (unicodedata.normalize('NFD', key).encode('ascii', 'ignore')).decode("utf-8")
    print(key2)
    if ' ' in key2:
        query = '"' + key2.replace('-', ' ') + '"'
    else:
        query = key2
    url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=IN%2F' + query + '&d=PTXT'

    try:
        driver.get(url)
        r1 = driver.page_source
        sleep(1)
        r2 = driver.page_source
        s1 = BeautifulSoup(r1, 'html.parser')
        s2 = BeautifulSoup(r2, 'html.parser')
        # print('First')
        # print(s1)
        # print('Wait')
        # print(s2)

        patents = []

        if s1.find(string=re.compile('No patents have matched your query')):
            print('No results')
        elif s1.find(string=re.compile('Single Document')):
            #print('S1')
            string = s2.title.string.split(' ')
            patents.append(string[-1])
            # print(s2.find(string=re.compile('United States Patent:')).find_next().text.strip())
        else:
            total_results = int(s1.find(string=re.compile('out of')).find_next().text.strip()) - 1
            print(total_results)
            for i, l in enumerate(s2.find_all(valign='top')):
                if i % 3 == 1:
                    patents.append(l.text.split('>')[0].replace(',', ''))

            for j in range(int(total_results/50)):
                # print(j)
                j = str(j + 2)
                ename = 'NextList'+j
                next_button = driver.find_element_by_name(ename)
                next_button.click()
                sleep(0.5)
                r2 = driver.page_source
                s2 = BeautifulSoup(r2, 'html.parser')
                #print(s2)
                for i, l in enumerate(s2.find_all(valign='top')):
                    if i % 3 == 1:
                        patents.append(l.text.split('>')[0].replace(',', ''))
    except:
        patents = []
    new_data[key] = [data[key], patents]

driver.quit()

with open('authors_with_patents_9.json', 'w') as json_file:
    json.dump(new_data, json_file)

