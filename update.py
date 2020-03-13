# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import os


def makeQuery():
    currentDate = datetime.now().strftime("%d.%m.%Y")
    query = "https://www.cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.FromDate=01.01.2015&UniDbQuery.ToDate=" + currentDate

    return query


def makeRequest(query):
    html_doc = urlopen(query).read()
    soup = BeautifulSoup(html_doc, features = "lxml")

    with open('parsed.txt', 'w', encoding = 'UTF-8') as parse:
        parse.write( str( soup.find('table', 'data') ) )

    return 'parsed.txt'


def makeDataFile():
    parse = makeRequest( makeQuery() )
    with open('data.txt', 'w', encoding = 'UTF-8') as outputFile:
        with open(parse, 'r', encoding = 'UTF-8') as inputFile:
            for line in inputFile:
                if line[:3] in ('<ta', '<tr', '<th', '</t'):
                    continue
                if line.find(',') == -1:
                    outputFile.write(line[4:14] + ' ')
                else:
                    outputFile.write(line[4:8] + '\n')

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), parse)
    os.remove(path)             


makeDataFile()
# html_doc = urlopen('https://www.cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.FromDate=01.01.2015&UniDbQuery.ToDate=13.03.2020').read()
# soup = BeautifulSoup(html_doc, features="lxml")
# print( soup.find('table', 'data') )
