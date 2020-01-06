import json
import re
import unicodedata
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup
from elasticsearch import helpers
from flask_login import UserMixin
from werkzeug.routing import BaseConverter


def write_html(key, dict_values):
    fn = open('./templates/name_results.html', 'w', encoding='utf-8')
    string = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>
<button onclick="goBack()">Go Back</button>
<script>
function goBack() {
window.history.back();
}
</script>
</h1>
    '''

    name = key.split('-')[1] + ' ' + key.split('-')[0]
    string += '<h2> Name:</h2>'
    string += name + '\n'
    string += '<h2> Affiliation:</h2><ul>'
    for p in dict_values[0]:
        string += '<li><p> ' + str(p).replace(',', '</p><p>') + '</p></li>'
    string += '</ul><h2> Publications (' + str(len(dict_values[1])) + '):</h2><ul>'
    publications = sorted(dict_values[1], reverse=True)
    if len(publications) < 10:
        for p in dict_values[1]:
            string += '<li><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + str(p) + '"> ' + str(p) + '</a></li>'
    else:
        for p in publications[:10]:
            string += '<li><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + str(p) + '"> ' + str(p) + '</a></li>'
        string += '</ul><details><summary> See More </summary><ul>'
        for p in publications[10:]:
            string += '<li><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + str(p) + '"> ' + str(p) + '</a></li>'
        string += '</details>'

    string += '</ul><h2> Patents:</h2><ul>'
    print(key)
    key2 = (unicodedata.normalize('NFD', key).encode('ascii', 'ignore')).decode("utf-8")
    print(key2)
    if ' ' in key2:
        query = '"' + key2.replace('-', ' ') + '"'
    else:
        query = key2
    url = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2F' \
          'search-adv.htm&r=0&p=1&f=S&l=50&Query=IN%2F' + query + '&d=PTXT'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        s1 = BeautifulSoup(the_page, 'html.parser')
        patents = []
        if s1.find(string=re.compile('No patents have matched your query')):
            print('No results')
        elif s1.find(string=re.compile('Single Document')):
            #print('S1')
            redirect = s1.find('meta').get('content').split('URL=')[1]
            url2 = 'http://patft.uspto.gov/' + redirect
            req = urllib.request.Request(url2)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            s2 = BeautifulSoup(the_page, 'html.parser')
            strings = s2.title.string.split(' ')
            patents.append(strings[-1])
            # print(s2.find(string=re.compile('United States Patent:')).find_next().text.strip())
        else:
            total_results = int(s1.find(string=re.compile('out of')).find_next().text.strip()) - 1
            print(total_results)
            for i, l in enumerate(s1.find_all(valign='top')):
                if i % 3 == 1:
                    patents.append(l.text.split('>')[0].replace(',', ''))

            # for j in range(int(total_results/50)):
            #     # print(j)
            #     j = str(j + 2)
            #     ename = 'NextList'+j
            #     next_button = driver.find_element_by_name(ename)
            #     next_button.click()
            #     sleep(0.5)
            #     r2 = driver.page_source
            #     s2 = BeautifulSoup(r2, 'html.parser')
            #     #print(s2)
            #     for i, l in enumerate(s2.find_all(valign='top')):
            #         if i % 3 == 1:
            #             patents.append(l.text.split('>')[0].replace(',', ''))

    except:
        patents = []

    for p in patents:
        string += '<li><a href="http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnet' \
                  'ahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1='+str(p)+'.PN.&OS=PN/'+str(p)+'&RS=PN/'+str(p) + '"> ' + \
                  str(p) + '</a></li>'
    string += '</ul><h2> Top co-authors:</h2>'

    string += '</ul><h2> Most cited publications:</h2>'
    # string += '<h2> Citations:</h2>'

    string += '''
</body>
</html>
    '''
    fn.write(string)


def write_table(df):
    fname = open('./templates/key_results.html', 'w', encoding='utf-8')
    columns = df.columns
    string = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 90%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    
    tr:nth-child(even) {
      background-color: #dddddd;
    }
    
    th.fitwidth0 {
        width: 15%
    }
    th.fitwidth1 {
        width: 45%
    }
    th.fitwidth2 {
        width: 20%
    }
    th.fitwidth3 {
        width: 20%
    }
    
    </style>
    </head>
    <body>

    <h1>
    <button onclick="goBack()" class="btn">Go Back</button>
    <button onclick="exportTableToCSV('selected_data.csv')" class="btn">Export HTML Table To CSV File</button>
    <script>
    function goBack() {
    window.history.back();
    }
    </script>
    </h1>
    
    <script src="https://www.w3schools.com/lib/w3.js"></script>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet" />
    '''
    string += "<h1>Top " + str(
        df.shape[0]) + ' results </h1> <ul>\n<table align="center" id="usersTable" class="w3-table-all">\n<tr>'

    for i, c in enumerate(columns):
        # string += '''<th onclick="w3.sortHTML('#usersTable', '.item', 'td:nth-child(''' + str(
        string += '''<th class="fitwidth''' + str(i) + '''" style="cursor:pointer"> ''' + \
                  str(c) + '</th>\n'
    string += '</tr>\n'
    df = df[:200]
    for vs in df.values:
        string += '<tr class="item">\n'
        for i, v in enumerate(vs):
            # print(i, v)
            if i == 0:
                key = str(v).replace(', ', '-')
                string += '''<td><a href="{{ url_for('cap_search', key =' ''' + key + ''' ') }}">''' + str(v) + '</a></td>'
            elif i == 1:
                if len(v) > 0:
                    string += '<td>' + str(v[0]).replace(',', ';') + '</td>\n'
                else:
                    string += '<td> Not available </td>\n'
            elif i == 2 or i == 3:
                string += '<td><ul>'
                lps = False
                if len(v) > 10:
                    ps = str(len(v))
                    v = v[:10]
                    lps = True
                for v2 in v:
                    if v2 == -1:
                        v3 = 'Not available'
                    else:
                        v3 = v2
                    string += '<li><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + str(v3) + '">' + str(v3) + '</a></li>'
                if lps:
                    string += '<li><a> ... (' + ps + ') </a></li>'
                string += '</ul></td>\n'
            else:
                string += '<td>' + str(v) + '</td>\n'
        string += '</tr>\n'

    string += '''
    </table>

    <script>
        function downloadCSV(csv, filename) {
        var csvFile;
        var downloadLink;

        // CSV file
        csvFile = new Blob([csv], {type: "text/csv"});

        // Download link
        downloadLink = document.createElement("a");

        // File name
        downloadLink.download = filename;

        // Create a link to the file
        downloadLink.href = window.URL.createObjectURL(csvFile);

        // Hide download link
        downloadLink.style.display = "none";

        // Add the link to DOM
        document.body.appendChild(downloadLink);

        // Click download link
        downloadLink.click();
    }

    function exportTableToCSV(filename) {
        var csv = [];
        var rows = document.querySelectorAll("table tr");

        for (var i = 0; i < rows.length; i++) {
            var row = [], cols = rows[i].querySelectorAll("td, th");

            for (var j = 0; j < 2; j++)
                row.push(cols[j].innerText);

            csv.push(row.join(","));
        }

        // Download CSV file
        downloadCSV(csv.join("\\n"), filename);
    }


    </script>

    </ul>
    </body>
    </html>
    '''
    fname.write(string)


def write_new_table(df):
    fname = open('./templates/new_key_results.html', 'w', encoding='utf-8')
    columns = df.columns
    string = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 90%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }

    th.fitwidth0 {
        width: 15%
    }
    th.fitwidth1 {
        width: 25%
    }
    th.fitwidth2 {
        width: 20%
    }
    th.fitwidth3 {
        width: 20%
    }

    </style>
    </head>
    <body>

    <h1>
    <button onclick="goBack()" class="btn">Go Back</button>
    <button onclick="exportTableToCSV('selected_data_nih.csv')" class="btn">Export HTML Table To CSV File</button>
    <script>
    function goBack() {
    window.history.back();
    }
    </script>
    </h1>

    <script src="https://www.w3schools.com/lib/w3.js"></script>
    <link href="https://www.w3schools.com/w3css/4/w3.css" rel="stylesheet" />
    '''
    string += "<h1>Top " + str(
        df.shape[0]) + ' results </h1> <ul>\n<table align="center" id="usersTable" class="w3-table-all">\n<tr>'

    for i, c in enumerate(columns):
        # string += '''<th onclick="w3.sortHTML('#usersTable', '.item', 'td:nth-child(''' + str(
        string += '''<th class="fitwidth''' + str(i) + '''" style="cursor:pointer"> ''' + \
                  str(c) + '</th>\n'
    string += '</tr>\n'
    df = df[:200]
    for vs in df.values:
        string += '<tr class="item">\n'
        for i, v in enumerate(vs):
            # print(i, v)
            if i == 0:
                key = str(v).replace(', ', '-')
                string += '''<td>''' + str(
                    v) + '</td>'
            elif i == 1:
                if len(v) > 0:
                    string += '<td>' + str(v) + '</td>\n'
                else:
                    string += '<td> Not available </td>\n'
            elif i == 2 or i == 3:
                string += '<td><ul>'
                lps = False
                if len(v) > 10:
                    ps = str(len(v))
                    v = v[:10]
                    lps = True
                for v2 in v:
                    if v2 == -1:
                        v3 = 'Not available'
                    else:
                        v3 = v2
                    string += '<li><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + str(v3) + '">' + str(
                        v3) + '</a></li>'
                if lps:
                    string += '<li><a> ... (' + ps + ') </a></li>'
                string += '</ul></td>\n'
            elif i == 4:
                #print(v)
                string += '<td>'
                for v2 in v:
                    string += str(len(v2)) + ','
                string += '</td>\n'
            else:
                string += '<td>' + str(v) + '</td>\n'
        string += '</tr>\n'

    string += '''
    </table>

    <script>
        function downloadCSV(csv, filename) {
        var csvFile;
        var downloadLink;

        // CSV file
        csvFile = new Blob([csv], {type: "text/csv"});

        // Download link
        downloadLink = document.createElement("a");

        // File name
        downloadLink.download = filename;

        // Create a link to the file
        downloadLink.href = window.URL.createObjectURL(csvFile);

        // Hide download link
        downloadLink.style.display = "none";

        // Add the link to DOM
        document.body.appendChild(downloadLink);

        // Click download link
        downloadLink.click();
    }

    function exportTableToCSV(filename) {
        var csv = [];
        var rows = document.querySelectorAll("table tr");

        for (var i = 0; i < rows.length; i++) {
            var row = [], cols = rows[i].querySelectorAll("td, th");

            for (var j = 0; j < 2; j++)
                row.push(cols[j].innerText);

            csv.push(row.join(","));
        }

        // Download CSV file
        downloadCSV(csv.join("\\n"), filename);
    }


    </script>

    </ul>
    </body>
    </html>
    '''
    fname.write(string)


def get_citations():
    from selenium import webdriver

    driver = webdriver.Chrome(r'C:\Users\jchaves6\PycharmProjects\Retention\chromedriver')

    with open('authors_9.json') as json_file:
        data = json.load(json_file)
    new_data = data
    ik = 0
    for k in data.keys():
        ik += 1
        if ik < 100:
            continue
        if ik > 600:
            break
        affiliations, papers, titles, abstracts, citations, urls = data[k]
        cit2 = []
        for url, cit in zip(urls, citations):
            if cit != -1:
                print('skip')
                cit2.append(cit)
                continue
            driver.get(url)
            cits = 0
            try:
                citation = driver.find_element_by_class_name('cited-by-count')
                cits = int(citation.text.split(' ')[-1])
            except:
                try:
                    citation = driver.find_element_by_class_name('articleMetrics_count')
                    cits = int(citation.text.split('\n')[1])
                except:
                    try:
                        citation = driver.find_element_by_class_name('__dimensions_Badge_stat_count')
                        cits = int(citation.text)
                    except:
                        try:
                            citation = driver.find_element_by_class_name('pps-count')
                            cits = int(citation.text)
                        except:
                            try:
                                citation = driver.find_element_by_css_selector('[data-test="citation-count"]')
                                cits = int(citation.text.split(' ')[0])
                            except:
                                print('No citations', url)
                                cits = -1
            # print('cits=', cits)
            cit2.append(cits)

        new_data[k] = [affiliations, papers, titles, abstracts, cit2, urls]

    with open('authors_9.json', 'w') as json_file:
        json.dump(new_data, json_file)


def worker(arg):
    keyword, num = arg
    """thread worker function"""
    filename = './authors_' + str(num)+'.json'
    print(filename)
    with open(filename) as json_file:
        data = json.load(json_file)

    if keyword != '':
        new_data = {}
        # [affiliations, papers, titles, abstracts, citations]
        for k in data.keys():
            papers = []
            titles = []
            abstracts = []
            citations = []
            for p, t, a, c in zip(data[k][1], data[k][2], data[k][3], data[k][4]):
                if t is None or a is None:
                    continue
                if keyword in t.lower() or keyword in a.lower():
                    papers.append(p)
                    titles.append(t)
                    abstracts.append(a)
                    citations.append(c)
            if len(papers) > 0:
                try:
                    aff = data[k][0][0]
                except:
                    aff = ''
                new_data[k] = [aff, papers, citations]
    else:
        new_data = {}
        for k in data.keys():
            affiliations, papers, titles, abstracts, citations, urls = data[k]
            try:
                aff = affiliations[0]
            except:
                aff = ''
            new_data[k] = [aff, papers, citations]
        max_res = 199

    return new_data


def search_dataframe(arg):
    keyword, num = arg
    filename = './publication_files/publications_' + num + '.pkl'
    # print(filename)
    df = pd.read_pickle(filename)

    if keyword != '':
        return df[(df['title'].map(lambda x: keyword in x)) | (df['abstract'].map(lambda x: keyword in x))]
    else:
        return df


def search_new_dataframe(arg):
    keyword, year = arg
    # filename = './publication_files/publications_' + num + '.pkl'
    filename = './project_files/projects_' + year + '.pkl'
    # print(filename)
    df = pd.read_pickle(filename)

    if keyword != '':
        return df[(df['PROJECT_TITLE'].map(lambda x: keyword in x)) | (df['ABSTRACT_TEXT'].map(lambda x: keyword in x))]
    else:
        print('not found in df')
        return df


def read_dataframe(df):
    authors = {}
    # df = df[:10]
    # pudmid, title, abstract, authors, affiliations, url, citations
    for p, au, af, c in zip(df['pudmid'], df['authors'], df['affiliations'], df['citations']):
        for au2, af2 in zip(au, af):
            key = au2
            aff = af2
            if key in authors.keys():
                papers = authors[key][1]
                papers.append(p)
                citations = authors[key][2]
                citations.append(c)
                authors[key] = [aff, papers, citations]
            else:
                authors[key] = [aff, [p], [c]]
    return authors


def read_new_dataframe(df):
    authors = {}
    # df = df[:10]
    # pudmid, title, abstract, authors, affiliations, url, citations
    for p, au, af, c, tc, cs, pat in zip(df['APPLICATION_ID'], df['PI_NAMEs'], df['ORG_NAME'], df['Publications'],
                                         df['TOTAL_COST'], df['Clinical Studies'], df['Patents']):
        # print(p, au, af, c, tc)
        if len(au) < 5:
            continue
        key = au
        aff = af
        if key in authors.keys():
            projects = authors[key][1]
            projects.append(p)
            publications = authors[key][2]
            publications.append(c)
            total_costs = authors[key][3]
            total_costs.append(tc)
            clinical_studies = authors[key][4]
            clinical_studies.append(cs)
            patents = authors[key][5]
            patents.append(pat)
            authors[key] = [aff, projects, publications, total_costs, clinical_studies, patents]
        else:
            authors[key] = [aff, [p], [c], [tc], [cs], [pat]]
    return authors


def read_new_esdataframe(df):
    authors = {}
    # df = df[:10]
    # pudmid, title, abstract, authors, affiliations, url, citations
    for p, au, af, c, tc, cs, pat in zip(df['APPLICATION_ID'], df['AUTHOR'], df['AFFILIATION'], df['Publications'],
                                         df['FUNDING'], df['Clinical Studies'], df['Patents']):
        # print(p, au, af, c, tc)
        if len(au) < 5:
            continue
        key = au
        aff = af
        if key in authors.keys():
            projects = authors[key][1]
            projects.append(p)
            publications = authors[key][2]
            publications.append(c)
            total_costs = authors[key][3]
            total_costs.append(tc)
            clinical_studies = authors[key][4]
            clinical_studies.append(cs)
            patents = authors[key][5]
            patents.append(pat)
            authors[key] = [aff, projects, publications, total_costs, clinical_studies, patents]
        else:
            authors[key] = [aff, [p], [c], [tc], [cs], [pat]]
    return authors


def init_projects_indices(esclient):
    if not esclient:
        return
    df = pd.read_pickle('./project_files/projects_2018.pkl')
    print(df.shape[0])
    string = ''
    df2 = df
    actions = []
    for d in df2.values:
        action = {
            "_index": "projs-index",
            "_type": "projects",
            "_id": d[0],
            "_source": {
                'APPLICATION_ID': d[0],
                'PROJECT_TITLE': d[35],
                'ABSTRACT_TEXT': d[-4],
                'PI_NAMEs': d[30],
                'ORG_NAME': d[25],
                'Publications': d[-3],
                'TOTAL_COST': d[-6] if isinstance(d[-6], float) else -1,
                'Clinical Studies': d[-2],
                'Patents': d[-1]
            }
        }

        actions.append(action)

    helpers.bulk(esclient, actions)


def project_elasticsearch(esclient, keyword, max_res):
    if not esclient:
        return
    response = esclient.search(
        index='projs-index',
        body={
            "query": {
                # "bool": {
                #     "must": [
                #         { "match": { "age": "40" } }
                #     ],
                #     "must_not": [
                #         { "match": { "state": "ID" } }
                #     ]
                # }
                "multi_match": {
                    "query": keyword,
                    "fields": ["ABSTRACT_TEXT", "PROJECT_TITLE"],
                }
            },
            "size": 10000
        }
    )

    print(response['hits']['total'], 'took=', response['took'])
    print(response['hits']['hits'][0], 'took=', response['took'])

    df = pd.DataFrame(columns=['SCORE', 'APPLICATION_ID', 'AUTHOR', 'AFFILIATION', 'FUNDING', 'Publications',
                               'Clinical Studies', 'Patents'])

    for hit in response['hits']['hits']:
        # print(hit['_score'], hit['_source']['APPLICATION_ID'])
        df = df.append({'SCORE': hit['_score'],
                        'APPLICATION_ID': hit['_source']['APPLICATION_ID'],
                        'AUTHOR': hit['_source']['PI_NAMEs'],
                        'AFFILIATION': hit['_source']['ORG_NAME'],
                        # 'Publications': d[-3],
                        'FUNDING': hit['_source']['TOTAL_COST'],
                        'Publications': hit['_source']['Publications'],
                        'Clinical Studies': hit['_source']['Clinical Studies'],
                        'Patents': hit['_source']['Patents']

                        }, ignore_index=True)

    # print(df.head())
    return df
    # return response['hits']


class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(self, value)
                        for value in values)


if __name__ == '__main__':
    get_citations()
