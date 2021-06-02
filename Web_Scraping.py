import re
import ssl

import requests
from bs4 import BeautifulSoup
import bs4
import metadata_parser

DEFAULT_TIMEOUT = 100

#pg = requests.get("https://gitconnected.com/learn/python")
#print(pg.status_code)

#soup = BeautifulSoup(pg.content, 'html.parser')

#print(soup.find("title").string)
#print(soup.find("meta", attrs={"name":'description'})['content'])
#print(soup.find("meta", attrs={"name":'keywords'})['content'])
#for a in soup.find_all('a', href=True):
#    print(a["href"])


def title(soup):
    try:
        return soup.find("title").string
    except:
        return "something went wrong in title"


def learningtypes(soup):
    return


def datatopics(s):
    topics=[]
    return


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
        print(re.findall("\$[\d,]*\.\d\d", soup.prettify()))
        return re.findall("\$[\d,]*\.\d\d", soup.prettify())


def vendor(soup):
    return


def publicdod(soup):
    return


def timecom(soup):
    return


def certificate(soup):
    return


def language(soup):
    return


def operations(soup):
    return


def barrier(soup):
    return


def selfinstructor(soup):
    return


def learningtype(soup):
    return


def inpersonremote(soup):
    return



def useful(soup):

    return


def main(a):
    bigarray = []
    for website in a:
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
            array.append(datatopics(soup))
            array.append(language(soup))
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
    return bigarray


def youtube(a):
    search = a
    x = 0
    urlarrays = []
    while x <= 100:
        url = f"https://www.youtube.com/results?search_query={search}"
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text,
                                 "html.parser")
        heading_object = soup.find_all('a', href=True)
        for info in heading_object:
            url = info["href"]
            if "https" in url:
                urlstart = url.find("h")
                urlend = url.find("&sa")
                url = url[urlstart:urlend]
                if "google" not in url:
                    if url not in urlarrays:
                        urlarrays.append(url)
        x += 10
    return urlarrays


def google(a):
    search = a
    x = 0
    urlarrays = []
    while x <= 10:
        url = f"https://www.google.com/search?&q={search}&start=" + str(x)
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text,
                                 "html.parser")
        heading_object = soup.find_all('a', href=True)
        for info in heading_object:
            url = info["href"]
            if "https" in url:
                urlstart = url.find("h")
                urlend = url.find("&sa")
                url = url[urlstart:urlend]
                if "google" not in url:
                    if url not in urlarrays:
                        urlarrays.append(url)
        x += 10
    print("done googling!!!")
    return urlarrays


def test(a):
    try:
        req=requests.get(a)
        soup = bs4.BeautifulSoup(requests.get(a).text, "html.parser")
        print(soup.prettify())
       #print(re.findall("\$\d*\.\d\d", soup.prettify()))
    except requests.exceptions.SSLError:
        print("does it hit this one?")
    except requests.exceptions.MissingSchema:
        print("USnews?????")


if __name__ == '__main__':
    print(main(google("Python Data Analysis Courses")))
    #page= metadata_parser.MetadataParser('https://www.coursera.org/learn/python')
    #print(page.metadata)

