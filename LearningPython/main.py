import requests
from bs4 import BeautifulSoup

def web_scrapper(weblink):

    response = requests.get(weblink)

    soup = BeautifulSoup(response.content, 'html.parser')

    tag = soup.title
    type(tag)
    print(soup.find("title").string)

    return response

web_scrapper("https://www.w3schools.com/python")