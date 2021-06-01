import requests
from bs4 import BeautifulSoup

#pg = requests.get("https://gitconnected.com/learn/python")
#print(pg.status_code)

#soup = BeautifulSoup(pg.content, 'html.parser')

#print(soup.find("title").string)
#print(soup.find("meta", attrs={"name":'description'})['content'])
#print(soup.find("meta", attrs={"name":'keywords'})['content'])
#for a in soup.find_all('a', href=True):
#    print(a["href"])

def title(soup):
    return soup.find("title").string

def formats(soup):
    return False

def description(soup):
    if soup.find("meta", attrs={"name":'description'}):
        return soup.find("meta", attrs={"name":'description'})['content']


def main(a):
    bigarray = []
    for website in a:
        array = []
        array.append(website)
        html = requests.get(website)
        soup = BeautifulSoup(html.content, 'html.parser')
        array.append(title(soup))
        #array.append(formats(soup))
        array.append(description(soup))
        bigarray.append(array)
    return bigarray

if __name__ == '__main__':
    print(main(["https://www.youtube.com/watch?v=kWyoYtvJpe4", "https://www.youtube.com/watch?v=uKZ8GBKmeDM", "https://www.professormesser.com/security-plus/sy0-601/sy0-601-video/sy0-601-comptia-security-plus-course/", "https://stackoverflow.com/questions/45137395/how-do-i-upgrade-the-python-installation-in-windows-10", "https://www.w3schools.com/python/default.asp"]))
