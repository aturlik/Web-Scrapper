import re
import ssl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import bs4
import metadata_parser
import random
import xlsxwriter

DEFAULT_TIMEOUT = 100


topics = ['statistics', 'machine learning', 'data analytics', 'image analysis', 'regression', 'classification','database','visualization','data science','natural language processing','computer vision','image generation','robotics']

subsection = ['course','training','guide','tutorial','instruction']

language = ['python','java','matlab','R','C','C++','Julia','Labview','SAS','COMSOL']



def searchtermcombo():
    lan=random.choice(language)
    top=random.choice(topics)
    sub=random.choice(subsection)
    return (top,lan,sub)


def title(soup):
    try:
        return soup.find("title").string
    except:
        return "something went wrong in title"


def learningtypes(soup):
    return "Null"


def datatopics(s):
    topics=[]
    return "Null"


def description(soup):
    try:
        if soup.find("meta", attrs={"name":'description'}):
            return soup.find("meta", attrs={"name":'description'})['content']
    except:
        return "something broke in description"


def keywords(soup):
    try:
        if soup.find("meta", attrs={"name":'keywords'}):
            return soup.find("meta", attrs={"name":'keywords'})['content']
    except:
        return "something went wrong in keywords"


def cost(soup):
    # print(re.findall("\$[\d,]*\.\d\d", soup.prettify()))
    moneyarray = re.findall("\$[\d,]*\.\d\d", soup.prettify())
    finalarray = set(moneyarray)
    print(list(finalarray))
    return list(finalarray)


def vendor(soup):
    return "Null"


def publicdod(soup):
    return "Null"


def timecom(soup):
    return "Null"


def certificate(soup):
    return "Null"


def languagetype(soup):
    languages = ['Python', 'Java', 'Matlab', 'R', 'C', 'C++', 'Julia', 'LabVIEW', 'SAS', 'COMSOL']
    for L in languages:
        if L in searchterm or L in title(soup):
            return L
        else:
            return "Null"


def operations(soup):
    return "Null"


def barrier(soup):
    return "Null"


def selfinstructor(soup):
    return "Null"


def learningtype(soup):
    return "Null"


def inpersonremote(soup):
    return "Null"



def useful(soup):
    return "Null"


def main(a):
    bigarray = []
    for website in a[0]:
        array = []
        try:
            print("starting to scrape", website)
            html = requests.get(website, timeout=5)
            soup = BeautifulSoup(html.content, 'html.parser')
            ###############################
            array.append(title(soup))
            array.append(website)
            array.append(vendor(soup))
            array.append(cost(soup))
            array.append(publicdod(soup))
            array.append(timecom(soup))
            array.append(certificate(soup))
            # array.append(datatopics(soup,a[1]))
            array.append(a[1])
            array.append(a[2])
            # array.append(languagetype(soup,a[2]))
            array.append(operations(soup))
            array.append(barrier(soup))
            array.append(selfinstructor(soup))
            array.append(learningtype(soup))
            array.append(inpersonremote(soup))
            array.append(useful(soup))
            array.append((description(soup), keywords(soup)))
            ##################
            bigarray.append(array)
            print("done scraping", website)
        except requests.exceptions.SSLError:
            print("\n----------ERROR SSL ERROR----------\n")
        except requests.exceptions.ReadTimeout:
            print("\n----------ERROR TIME OUT ERROR----------\n")
        except requests.exceptions.ConnectionError:
            print("\n----------ERROR CONNECTION ERROR----------\n")
        except TypeError:
            print("\n----------ERROR UNABLE TO READ ERROR----------\n")
    return bigarray




def google():
    tuplesearch=searchtermcombo()
    search = '%s %s %s' % (tuplesearch[0],tuplesearch[1],tuplesearch[2])
    print("search terms are:", search)
    x = 0
    urlarrays = []
    while x <= 100:
        url = f"https://www.google.com/search?&q={search}&start=" + str(x)
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text,
                                 "html.parser")
        heading_object = soup.find_all('a', href=True)
        blacklist = ['google','reddit','facebook','pdf']
        for info in heading_object:
            url = info["href"]
            if "https" in url:
                urlstart = url.find("h")
                urlend = url.find("&sa")
                url = url[urlstart:urlend]
                #if blacklist not in url:
                if any(word in url for word in blacklist):
                    print("Blacklist hit")
                else:
                    if url not in urlarrays:
                        urlarrays.append(url)
        x += 10
    print("done googling!!!")
    return urlarrays,tuplesearch[0],tuplesearch[1]


def sendtospreadsheet(a):
    df = pd.DataFrame(a)
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    writer.save()

def test(a):
    try:
        soup = bs4.BeautifulSoup(requests.get(a).text, "html.parser")
        print(soup.prettify())
       #print(re.findall("\$\d*\.\d\d", soup.prettify()))
    except requests.exceptions.SSLError:
        print("does it hit this one?")
    except requests.exceptions.MissingSchema:
        print("USnews?????")


if __name__ == '__main__':
    array = main(google())
    #print(array)
    sendtospreadsheet(array)
    #page= metadata_parser.MetadataParser('https://www.coursera.org/learn/python')
    #print(page.metadata)

