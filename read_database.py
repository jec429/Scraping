import xml.etree.ElementTree as Et
import json
import sys
import gzip
import glob
from selenium import webdriver
import numpy as np
import pandas as pd
import time
import zipfile
import itertools

import multiprocessing as mp
from string import ascii_uppercase


def read_authors(num):
    authors = {}
    # driver = webdriver.Chrome(r'C:\Users\jchaves6\PycharmProjects\Retention\chromedriver')

    for fn in glob.glob('./database/pubmed19n0'+str(num)+'.xml.gz'):
        print(fn)

        file_content = gzip.open(fn, 'r')
        tree = Et.parse(file_content)

        root = tree.getroot()
        test = root.findall('./PubmedArticle/MedlineCitation/Article')
        test2 = root.findall('./PubmedArticle/MedlineCitation/PMID')
        test3 = root.findall('./PubmedArticle/PubmedData/ArticleIdList')

        print(len(test), len(test2), len(test3))

        ia = 0
        for t1, t2, t3 in zip(test, test2, test3):
            # print('New Article')
            # print(t2.text)
            if ia % 1000 == 0:
                print('%d/%d' % (ia, len(test)))

            al = t1.find('AuthorList')
            if al is None:
                continue

            at = t1.find('ArticleTitle')
            title = ''
            if at is not None:
                title = at.text
            ab = t1.find('Abstract')
            abstract = ''
            if ab is not None:
                abstract = ab.find('AbstractText').text
            cits = -1
            url = ''
            for d in t3:
                if d.attrib['IdType'] == 'doi':
                    url = 'http://doi.org/' + d.text
                    #print(d.attrib, d.text, url)
                    #driver.get(url)
                    citation = None
                    try:
                        #citation = driver.find_element_by_class_name('cited-by-count')
                        cits = int(citation.text.split(' ')[-1])
                    except:
                        try:
                            #citation = driver.find_element_by_class_name('articleMetrics_count')
                            cits = int(citation.text.split('\n')[1])
                        except:
                            try:
                                # citation = driver.find_element_by_class_name('__dimensions_Badge_stat_count')
                                cits = int(citation.text)
                            except:
                                continue
                                #print('No pubs')

            for author in al:
                key = ''
                aff = []
                # for n in author:
                #     if n.text is None:
                #         continue
                #     print(n, n.text)
                #     if n.tag == 'AffiliationInfo':
                #         for a in n:
                #           aff.append(a)
                #
                #    key += n.text.replace(' ', '')

                ln = author.find('LastName')
                fn = author.find('ForeName')
                af = author.find('AffiliationInfo')
                if af is not None:
                    for a in af:
                        # print(af, a.text)
                        aff.append(a.text)
                if ln is None or fn is None:
                    continue
                key = ln.text + '-' + fn.text.replace(' ', '')
                # print('Key=', key)

                if key not in authors:
                    authors[key] = [aff, [t2.text], [title], [abstract], [cits], [url]]
                else:
                    affiliations = authors[key][0]
                    papers = authors[key][1]
                    papers.append(t2.text)
                    titles = authors[key][2]
                    titles.append(title)
                    abstracts = authors[key][3]
                    abstracts.append(abstract)
                    citations = authors[key][4]
                    citations.append(cits)
                    urls = authors[key][5]
                    urls.append(url)
                    authors[key] = [affiliations, papers, titles, abstracts, citations, urls]

            ia += 1

    with open('authors_'+str(num)+'.json', 'w') as json_file:
        json.dump(authors, json_file)


def read_publication(num):
    import os.path

    for fn in glob.glob('./database/pubmed19n0972.xml.gz'):
        ifile = fn.replace('\\', '/').split('n0')[1].split('.')[0]
        fname = 'publications_' + str(ifile) + '.pkl'
        if os.path.isfile(fname):
            continue

        #fn = './database/pubmed19n0'+str(num)+'.xml.gz'
        fn = fn.replace('\\', '/')
        print(fn)
        data = []
        file_content = gzip.open(fn, 'r')
        tree = Et.parse(file_content)

        root = tree.getroot()
        test = root.findall('./PubmedArticle/MedlineCitation/Article')
        test2 = root.findall('./PubmedArticle/MedlineCitation/PMID')
        test3 = root.findall('./PubmedArticle/PubmedData/ArticleIdList')

        print(len(test), len(test2), len(test3))
        test = root.findall('./PubmedArticle/MedlineCitation/Article')
        test2 = root.findall('./PubmedArticle/MedlineCitation/PMID')
        test3 = root.findall('./PubmedArticle/PubmedData/ArticleIdList')
        ia = -1
        for t1, t2, t3 in zip(test, test2, test3):
            ia += 1
            #if ia > 100:
            #    break
            # print('New Article')
            # print(t2.text)
            if ia % 1000 == 0:
                print('%d/%d' % (ia, len(test)))

            al = t1.find('AuthorList')
            if al is None:
                continue

            at = t1.find('ArticleTitle')
            if at is None:
                continue
            if at.text is None:
                continue
            title = at.text.lower()

            ab = t1.find('Abstract')
            try:
                abstract = ab.find('AbstractText').text.lower()
            except:
                abstract = ''
            cits = -1
            url = ''
            for d in t3:
                if d.attrib['IdType'] == 'doi':
                    if d.text is None:
                        url = 'http://doi.org/'
                    else:
                        url = 'http://doi.org/' + d.text

            authors = []
            affiliations = []
            for author in al:
                key = ''
                aff = []

                ln = author.find('LastName')
                fn = author.find('ForeName')
                af = author.find('AffiliationInfo')
                if af is not None:
                    for a in af:
                        # print(af, a.text)
                        if a.text is None:
                            aff.append('')
                        else:
                            if len(a.text) > 100:
                                aff.append(a.text[:100])
                            else:
                                aff.append(a.text)
                if ln is None or fn is None:
                    continue
                if ln.text is None or fn.text is None:
                    continue
                key = ln.text + '-' + fn.text.split(' ')[0]
                authors.append(key)
                affiliations.append(aff)
            #print('New article')
            #print(title, abstract, authors, affiliations, url)

            data.append([t2.text, title, abstract, authors, affiliations, url])

        # print(data)

        df = pd.DataFrame(np.array(data), columns=['pudmid', 'title', 'abstract', 'authors', 'affiliations', 'url'])
        df['citations'] = -1
        df.info()
        #df.to_pickle('./publications_'+str(ifile)+'.pkl')
        df.to_csv('./publications_'+str(num)+'.csv', sep=',', encoding='utf-8')


def get_citations(df):
    # df = pd.read_pickle('publications_9.pkl')
    # df = df[:10]
    driver = webdriver.Chrome(r'C:\Users\jchaves6\PycharmProjects\Retention\chromedriver')
    driver.maximize_window()
    cit2 = []
    ind = -1
    first = df.shape[0] > 10
    for url, cit in zip(df['url'], df['citations']):
        ind += 1
        if ind % 100 == 0:
            print('%d/%d' % (ind, df.shape[0]))
        # if ind < nk*10:
        #     continue
        if ind < (df.shape[0] - 10) and first:
            continue
        if cit != -1:
            print('skip')
            cit2.append(cit)
            continue
        if url == '':
            continue
        driver.get(url)
        cits = 0
        try:
            citation = driver.find_element_by_class_name('cited-by-count')
            cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
        except:
            try:
                citation = driver.find_element_by_class_name('articleMetrics_count')
                cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
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
                            cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
                        except:
                            try:
                                citation = driver.find_element_by_class_name('citing-label')
                                cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
                            except:
                                try:
                                    elems = driver.find_elements_by_xpath("//a[@class='altmetric_details']")
                                    url2 = elems[0].get_attribute('href')
                                    driver.get(url2)
                                    citation = driver.find_element_by_class_name('scholarly-citation-counts')
                                    cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
                                except:
                                    try:
                                        driver.find_element_by_class_name('citedByEntry')
                                        cits = len(driver.find_elements_by_class_name('citedByEntry'))
                                    except:
                                        try:
                                            cits = int(driver.find_element_by_class_name('number').text)
                                        except:
                                            try:
                                                citation = driver.find_element_by_css_selector('[data-tabname="citedbyJump"]')
                                                cits = [int(s) for s in citation.text.split() if s.isdigit()][0]
                                            except:
                                                try:
                                                    citation = driver.find_element_by_id('citations-count-number')
                                                    cits = int(citation.text)
                                                except:
                                                    print('No citations', url)
                                                    cits = -1
        # print('cits=', cits)
        cit2.append(cits)
        df.iloc[ind, df.columns.get_loc('citations')] = cits

    # df['citations'] = cit2
    # df.to_pickle("./publications_9.pkl")
    #df.to_csv("./publications_9.csv", sep=',', encoding='utf-8')
    driver.close()
    return df


def read_dataframe():
    for fn in glob.glob('./publication_files/publications_*.pkl'):
        print(fn.split('_')[-1])
        ifn = fn.split('_')[-1].split('.')[0]
        start_time = time.time()
        authors = {}
        df = pd.read_pickle('./publication_files/publications_'+ifn+'.pkl')
        df.info()
        # df = df[:10]
        # pudmid, title, abstract, authors, affiliations, url, citations
        for p, au, af, c in zip(df['pudmid'], df['authors'], df['affiliations'], df['citations']):
            key = ''
            for au2, af2 in zip(au, af):
                key = au2
                aff = af2
                if key in authors.keys():
                    affiliation = authors[key][0]
                    papers = authors[key][1]
                    papers.append(p)
                    citations = authors[key][2]
                    citations.append(c)

                    authors[key] = [aff, papers, citations]
                else:
                    authors[key] = [aff, [p], [c]]

        print('Time =', time.time() - start_time)
        # print(authors)
        with open('./author_files/authors_'+ifn+'.json', 'w') as json_file:
           json.dump(authors, json_file)


def test_dataframe():
    start_time = time.time()
    keyword = 'brain cancer'

    df = pd.read_pickle('publications_901.pkl')
    # df.info()
    # df1 = df[(df['title'].str.contains(keyword) | df['abstract'].str.contains(keyword))]
    # print(df1.head())
    # print('Time =', time.time() - start_time)
    # start_time = time.time()
    df2 = df[(df['title'].map(lambda x: keyword in x))]

    print('Time =', time.time() - start_time)
    start_time = time.time()
    df5 = pd.read_pickle('publications_901.pkl')

    df8 = df5[(df5['abstract'].map(lambda x: keyword in x))]

    print('Time =', time.time() - start_time)
    start_time = time.time()
    df5 = pd.read_pickle('publications_901.pkl')

    df8 = df5[(df5['title'].map(lambda x: keyword in x)) | (df5['abstract'].map(lambda x: keyword in x))]
    print('Time =', time.time() - start_time)


def merge_authors():
    authors = {}
    for fn in glob.glob('./author_files/authors_8*.json'):
        print(fn)
        with open(fn) as json_file:
            data = json.load(json_file)

        for key in data.keys():
            [aff, p, c] = data[key]
            if key in authors.keys():
                affiliation = authors[key][0]
                papers = authors[key][1]
                for p2 in p:
                    papers.append(p2)
                citations = authors[key][2]
                for c2 in c:
                    citations.append(c2)

                authors[key] = [aff, papers, citations]
            else:
                authors[key] = [aff, p, c]

    with open('./author_files/authors_comb_8.json', 'w') as json_file:
        json.dump(authors, json_file)


def split_by_key(ch):
    import pickle
    authors = {}
    print(ch)
    for fn in glob.glob('./author_files/authors_*.json'):
        print(fn)
        with open(fn) as json_file:
            data = json.load(json_file)

        for key in data.keys():
            if key[0] != ch:
                continue
            [aff, p, c] = data[key]
            if key in authors.keys():
                affiliation = authors[key][0]
                papers = authors[key][1]
                for p2 in p:
                    papers.append(p2)
                citations = authors[key][2]
                for c2 in c:
                    citations.append(c2)

                authors[key] = [aff, papers, citations]
            else:
                authors[key] = [aff, p, c]

    # with open('./author_files/authors_comb_A.json', 'w') as json_file:
    #     json.dump(authors, json_file)

    with open('./author_files/authors_comb_'+ch+'.pkl', 'wb') as f:
        pickle.dump(authors, f, pickle.HIGHEST_PROTOCOL)


def pre_fetch(keyword):
    # keyword, num = arg
    results = []
    for filename in glob.glob('./publication_files/publications_*.pkl'):
        print(filename)
        df = pd.read_pickle(filename)
        results.append(df[(df['title'].map(lambda x: keyword in x)) | (df['abstract'].map(lambda x: keyword in x))])
    joined_result = pd.concat(results)

    joined_result.to_pickle('./publications_' + keyword + '.pkl')
    joined_result.to_csv('./publications_' + keyword + '.csv', sep=',', encoding='utf-8')


def get_publications(args):
    df1, df2, df3, df4 = args
    pubs = []
    clinical_studies = []
    patents = []
    for p in df1['CORE_PROJECT_NUM']:
        # print(p)
        # print(df3[df3['PROJECT_NUMBER'].str.contains(p)]['PMID'].to_list())
        pubs.append(df2[df2['PROJECT_NUMBER'].str.contains(p)]['PMID'].to_list())
        clinical_studies.append(df3[df3['Core Project Number'].str.contains(p)]['ClinicalTrials.gov ID'].to_list())
        patents.append(df4[df4['PROJECT_ID'].str.contains(p)]['PATENT_ID'].to_list())
    # print(df3.shape[0])
    # df3 = df3[df3['PROJECT_NUMBER'].str.contains(p)==False]
    # iev += 1
    return pubs, clinical_studies, patents


def merge_nih(year):
    df1 = pd.read_csv('database/nihdata/RePORTER_PRJ_C_FY'+str(year)+'.zip', encoding="ISO-8859-1")
    df2 = pd.read_csv('database/nihdata/RePORTER_PRJABS_C_FY' + str(year) + '.zip', encoding="ISO-8859-1")
    # Check for files in the future since there are publications that happen in the future years
    df3 = pd.read_csv('database/nihdata/RePORTER_PUBLNK_C_' + str(year) + '.zip', encoding="ISO-8859-1")
    df4 = pd.read_csv('database/nihdata/RePORTER_CLINICAL_STUDIES_C_ALL.zip', encoding="ISO-8859-1")
    df5 = pd.read_csv('database/nihdata/RePORTER_PATENTS_C_ALL.zip', encoding="ISO-8859-1")
    # df1.info()
    # df2.info()
    result = df1.merge(df2, on=['APPLICATION_ID'])
    result.info()
    df = result.fillna('N/A')
    #df = df[:9000]

    pool = mp.Pool(processes=(mp.cpu_count() - 1))
    results = pool.map(get_publications, [(df[:10000], df3, df4, df5),
                                          (df[10000:20000], df3, df4, df5),
                                          (df[20000:30000], df3, df4, df5),
                                          (df[30000:40000], df3, df4, df5),
                                          (df[40000:50000], df3, df4, df5),
                                          (df[50000:60000], df3, df4, df5),
                                          (df[60000:70000], df3, df4, df5),
                                          (df[70000:80000], df3, df4, df5),
                                          (df[80000:], df3, df4, df5)
                                          ])
    pool.close()
    pool.join()

    pubs = results[0][0] + results[1][0] + results[2][0] + results[3][0] + results[4][0] + results[5][0] + results[6][0] + results[7][0] + results[8][0]
    clinical_studies = results[0][1] + results[1][1] + results[2][1] + results[3][1] + results[4][1] + results[5][1] + results[6][1] + results[7][1] + results[8][1]
    patents = results[0][2] + results[1][2] + results[2][2] + results[3][2] + results[4][2] + results[5][2] + results[6][2] + results[7][2] + results[8][2]

    # pubs = list(itertools.chain.from_iterable(results))
    # print(pubs)

    # for p in test_df['CORE_PROJECT_NUM']:
    #     if iev % 1000 == 0:
    #         print('%d/%d' % (iev, test_df.shape[0]))
    #     # print(p)
    #     # print(df3[df3['PROJECT_NUMBER'].str.contains(p)]['PMID'].to_list())
    #     pubs.append(df3[df3['PROJECT_NUMBER'].str.contains(p)]['PMID'].to_list())
    #     print(df3.shape[0])
    #     df3 = df3[df3['PROJECT_NUMBER'].str.contains(p)==False]
    #     iev += 1
    df['Publications'] = pubs
    df['Clinical Studies'] = clinical_studies
    df['Patents'] = patents
    # df.to_csv('test_db.csv', sep=',', encoding='utf-8')
    df.to_pickle('./project_files/projects_' + str(year) + '.pkl')


if __name__ == '__main__':
    # test_dataframe()
    start = time.time()
    # keyword = 'diabetic retinopathy'
    # pre_fetch(keyword)
    # read_publication(972)
    # for i in range(10):
    #     start = time.time()
    #     get_citations(i)
    #     print(time.time() - start)
    # get_citations(9)
    # for i in range(10):
    #    read_authors(900+i)

    # read_dataframe()
    # merge_authors()
    # for c in ascii_uppercase:
    #    split_by_key(c)
    # for j in range(100):
    #     print(j)
    #     df = pd.read_pickle('./publications_oncology.pkl')
    #     pool = mp.Pool(processes=(mp.cpu_count() - 1))
    #     i = 5 * j
    #     results = pool.map(get_citations, [df[:(i+1)*10],
    #                                        df[(i+1)*10:(i+2)*10],
    #                                        df[(i+2)*10:(i+3)*10],
    #                                        df[(i+3)*10:(i+4)*10],
    #                                        df[(i+4)*10:(i+5)*10]])
    #     pool.close()
    #     pool.join()
    #     results.append(df[(i+5)*10:])
    #     final_result = pd.concat(results)
    #     final_result.to_pickle("./publications_oncology.pkl")
    #     final_result.to_csv("./publications_oncology.csv", sep=',', encoding='utf-8')

    merge_nih(2018)

    print(time.time() - start)
