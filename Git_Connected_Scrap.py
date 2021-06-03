import requests
from bs4 import BeautifulSoup
import bs4

def gitconnected(a):
    search = a
    urlbigarrays = []
    urlarrays = []
    url = f"https://gitconnected.com/learn/{search}"
    print(url)
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    heading_object = soup.find_all('a', href=True)
    for info in heading_object:
        url = info["href"]
        if f'learn/{search}/' in url:
            url2 = "https://gitconnected.com" + url
            print('starting scraping ' + url2)
            req2 = requests.get(url2)
            soup2 = bs4.BeautifulSoup(req2.text, "html.parser")
            tags = soup2.find_all('span', attrs={'class':'tutorial-tag'})
            for i in range(len(tags)):
                tags[i] = tags[i].string
            urlarrays.append(tags)
            print('finish scraping')
            tags = []

        if "redirect" in url:
            if url not in urlarrays:
                urlarrays.append(url)
                urlarrays = []

        if urlarrays != []:
            urlbigarrays.append(urlarrays)

    return urlbigarrays

if __name__ == '__main__':
    print(gitconnected("python"))

