import requests
import bs4
import pandas as pd
import datetime
import xlsxwriter

def get_time():
    return datetime.datetime.now()

def get_title(soup2):
    title = soup2.find('h1', attrs={'class': 'ui header learn-tutorial-review-page__title'})
    return title.string

def get_link(soup2):
    urlblock = soup2.find('a', attrs={'class': 'ui fluid primary button'})
    urlblock = str(urlblock).split()
    urlname = urlblock[11]
    return urlname[7:-6]

def get_source(soup2):
    providername = soup2.find('div', attrs={'class': 'learn-tutorial-review-page__publisher'})
    provider = providername.find('span')
    return provider.string

def get_cost(soup2):
    tags = soup2.find_all('span', attrs={'class': 'tutorial-tag'})
    for i in range(len(tags)):
        tags[i] = tags[i].string
        if tags[i] == "Free":
            return "0"
        else:
            return ' '

def get_clear():
    return 'Public'

def get_tc():
    return ' '

def get_cert():
    return 'No'

def get_topic(search):
    # if search == 'data-structures-algorithms':
    #     return 'Tutorial, Data Structures'
    # elif search == 'artificial-intelligence-ai':
    #     return 'Tutorial, Artificial Intelligence'
    # else:
    return 'Tutorial, Cloud Services'

def get_language(search):
    # if search == 'c-plus-plus':
    #     return 'C++'
    # elif search == 'html-5':
    #     return 'HTML'
    # elif search == 'c-sharp':
    #     return 'C#'
    # elif search == 'linux-system-administration':
    #     return 'Linux'
    # elif search == 'assembly-language':
    #     return "Assembly"
    # elif search in ['data-structures-algorithms','artificial-intelligence-ai']:
    return ' '
    # else:
    #    return search.capitalize()

def get_bos():
    return 'Remote'

def get_level(soup2):
    tags = soup2.find_all('span', attrs={'class': 'tutorial-tag'})
    searchlist = ['Beginner','Advanced']
    for i in range(len(tags)):
        tags[i] = tags[i].string
        if tags[i] in searchlist:
            return tags[i]

def get_learningspeed():
    return "Self-paced"

def get_learning_type(soup2):
    tags = soup2.find_all('span', attrs={'class': 'tutorial-tag'})
    finaltag = []
    searchlist = ['Video', 'Book', 'Interactive Coding']
    for i in range(len(tags)):
        tags[i] = tags[i].string
        if tags[i] in searchlist:
            finaltag.append(tags[i])

    if len(finaltag) == 0:
        return ' '
    elif len(finaltag) == 1:
        return f'{finaltag[0]}'
    elif len(finaltag) == 2:
        return f'{finaltag[0]},{finaltag[1]}'

def get_remote():
    return 'Remote'

def get_useful():
    #score = soup2.find('div', attrs={'class': 'learn-tutorial-review-page__score-value'})
    #urlarrays.append(score.string)
    return 'Yes'

def get_desc(soup2):
    descript = soup2.find('p', attrs={'class': 'learn-tutorial-review-page__description'})
    return descript.string


def gitconnected(a):
    searchpool = a
    urlbigarrays = []
    urlarrays = []
    for search in searchpool:
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

                urlarrays.append(get_time())
                urlarrays.append(get_title(soup2))
                urlarrays.append(get_link(soup2))
                urlarrays.append(get_source(soup2))
                urlarrays.append(get_cost(soup2))
                urlarrays.append(get_clear())
                urlarrays.append(get_tc())
                urlarrays.append(get_cert())
                urlarrays.append(get_topic(search))
                urlarrays.append(get_language(search))
                urlarrays.append(get_bos())
                urlarrays.append(get_level(soup2))
                urlarrays.append(get_learningspeed())
                urlarrays.append(get_learning_type(soup2))
                urlarrays.append(get_remote())
                urlarrays.append(get_useful())
                urlarrays.append(get_desc(soup2))

                print('finish scraping')

            if "redirect" in url:
                urlarrays = []

            if urlarrays != []:
                urlbigarrays.append(urlarrays)

    return urlbigarrays

def sendtospreadsheet(a):
    df = pd.DataFrame(a)
    writer = pd.ExcelWriter('gitconnected.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    writer.save()

if __name__ == '__main__':
    # search = ['python','matlab','c-plus-plus','r','ruby','julia','java','c','javascript','html-5','c-sharp',\
    #           'linux-system-administration','arduino','assembly-language','data-structures-algorithms',\
    #           'artificial-intelligence-ai']
    search = ['amazon-web-services-aws']
    source = gitconnected(search)
    sendtospreadsheet(source)

