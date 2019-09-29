import xml.etree.ElementTree as Et
import json
import sys
import gzip
import glob
from selenium import webdriver
import numpy as np
import pandas as pd
import time
import multiprocessing as mp


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


def read_publication():
    data = []
    for fn in glob.glob('./database/pubmed19n0900.xml.gz')[:10]:
        print(fn)

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
            title = at.text

            ab = t1.find('Abstract')
            if ab is None:
                continue
            abstract = ab.find('AbstractText').text
            cits = -1
            url = ''
            for d in t3:
                if d.attrib['IdType'] == 'doi':
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
                        if len(a.text) > 100:
                            aff.append(a.text[:100])
                        else:
                            aff.append(a.text)
                if ln is None or fn is None:
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
    df.to_pickle("./publications_9.pkl")
    df.to_csv("./publications_9.csv", sep=',', encoding='utf-8')


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
    return df


def read_dataframe():
    authors = {}
    df = pd.read_pickle('publications_9.pkl')
    # df = df[:10]
    # pudmid, title, abstract, authors, affiliations, url, citations
    for p, t, a, au, af, u, c in zip(df['pudmid'], df['title'], df['abstract'], df['authors'], df['affiliations'], df['url'], df['citations']):
        key = ''
        for au2, af2 in zip(au, af):
            key = au2
            aff = af2
            if key in authors.keys():
                affiliation = authors[key][0]
                papers = authors[key][1]
                papers.append(p)
                titles = authors[key][2]
                titles.append(t)
                abstracts = authors[key][3]
                abstracts.append(a)
                citations = authors[key][4]
                citations.append(c)
                urls = authors[key][5]
                urls.append(u)
                authors[key] = [aff, papers, titles, abstracts, citations, urls]
            else:
                authors[key] = [aff, [p], [t], [a], [c], [u]]
    # print(authors)
    with open('authors_9.json', 'w') as json_file:
        json.dump(authors, json_file)


if __name__ == '__main__':
    # read_publication()
    # for i in range(10):
    #     start = time.time()
    #     get_citations(i)
    #     print(time.time() - start)
    # get_citations(9)
    # for i in range(10):
    #    read_authors(900+i)

    # read_dataframe()

    for j in range(190, 300):
        print(j)
        df = pd.read_pickle('publications_9.pkl')
        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        i = 5 * j
        results = pool.map(get_citations, [df[:(i+1)*10],
                                           df[(i+1)*10:(i+2)*10],
                                           df[(i+2)*10:(i+3)*10],
                                           df[(i+3)*10:(i+4)*10],
                                           df[(i+4)*10:(i+5)*10]])
        pool.close()
        pool.join()
        results.append(df[(i+5)*10:])
        final_result = pd.concat(results)
        final_result.to_pickle("./publications_9.pkl")
        final_result.to_csv("./publications_9.csv", sep=',', encoding='utf-8')
