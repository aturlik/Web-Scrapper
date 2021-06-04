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

#This section creates the topics, language, and subsection that will be randomly selected to use in our google searches for information on our database
topics = ['statistics', 'machine learning', 'data analytics', 'image analysis', 'regression', 'classification','database','visualization','data science','natural language processing','computer vision','image generation','robotics']

subsection = ['course','training','guide','tutorial','instruction']

language = ['python','java','matlab','R','C','C++','Julia','Labview','SAS','COMSOL']


#This creates a random string that will be searched for on google
def searchtermcombo():
    lan=random.choice(language)
    top=random.choice(topics)
    sub=random.choice(subsection)
    return (top,lan,sub)

#This looks through a websites HTML and attempts to find <title>, most sites have this and will return what the site is called
def title(soup):
    try:
        return soup.find("title").string
    except:
        return "something went wrong in title"

#This section determines what each site has as a topic
def datatopics(soup, topicsearched):
    #List of topics contain both capitolzied and uncapitolized words in hope to find site data topics more accurately
    topics = ['statistics', 'Statistics', 'stat', 'Stat', 'machine learning', 'Machine Learning', 'data analytics', 'Data Analytics', 'image analysis', 'Image Analysis', 'regression', 'Regression', 'classification', 'Classification', 'database', 'Database', 'visualization', 'Visualization', 'data science', 'Data Science', 'natural language processing', 'Natural Language Processing', 'computer vision', 'Computer Vision', 'image generation', 'Image Generation', 'robotics', 'Robotics']
    topicsused = "Null"
    #This segment looks if the topic is contained in the list
    for T in topics:
        if T in title(soup):
            topicsused = T
    #Honestly I don't think this if statements is needed but it does check if what we searched is the same as what the website is giving us
    if topicsused == topicsearched:
        return topicsearched
    #If the topic that was used on a site is not found it will just return null
    if topicsused == "Null":
        return "Null"
    #If a topic was not found for any of the topics in the list Null will be placed into the spreadsheet at the end
    if topicsused != "Null":
        return topicsused

#This function attempts to find a description from the site itself
def description(soup):
    #Placed in a try except statement because it breaks sometimes if the site isn't formated a certain way 
    try:
        #Many sites use the metadata tag of description making it easier to find descriptions but not all of them
        if soup.find("meta", attrs={"name":'description'}):
            return soup.find("meta", attrs={"name":'description'})['content']
    except:
        return "something broke in description"

#Find any keywords that the site may have
def keywords(soup):
     #Placed in a try except statement because it breaks sometimes if the site isn't formated a certain way 
    try:
        #Some sites that use keywords also keep them under the meta tag keywords
        if soup.find("meta", attrs={"name":'keywords'}):
            return soup.find("meta", attrs={"name":'keywords'})['content']
    except:
        return "something went wrong in keywords"

#This determines the cost that each site may have
def cost(soup):
    #this finds any instance of symbols in the shape of $###.### to find any underlying costs the site may have
    moneyarray = re.findall("\$[\d,]*\.\d\d", soup.prettify())
    finalarray = set(moneyarray)
    print(list(finalarray))
    return list(finalarray)

#Placecode to determine if a vendor can be found, at the moment returns null for the spreadsheet
def vendor(soup):
    return "Null"

#Most likely a tag we are getting rid of since all will be public on the interns side
def publicdod(soup):
    return "Public"

#Placecode to determine if time commitment can be found, at the moment returns null for the spreadsheet
def timecom(soup):
    return "Null"

#Placecode to determine if a certificate course can be determined by our scrapper, at the moment returns null for the spreadsheet
def certificate(soup):
    return "Null"

#Looks for what language the site is using to teach the topic
def languagetype(soup, languagesearched):
    #The single letter languages have a space after them so we know if the site is discussing the language or just has the letter
    languages = ['Python', 'Java', 'Matlab', 'R ', 'C ', 'C++ ', 'Julia', 'Labview', 'SAS', 'COMSOL']
    languageused = "Null"
    #Determines if one of the languages in our list is contained in the title of the website
    for L in languages:
        if L in title(soup):
            languageused = L
    #Much like the topic section this can be gotten rid of as it only determines if the language searched for is the one google found
    if languageused == languagesearched:
        return languagesearched
    #If no language in our list is found returns Null for the spreadsheet
    if languageused == "Null":
        return "Null"
    if languageused != "Null":
        return languageused

#Placecode to determine if operations can be found, at the moment returns null for the spreadsheet
def operations(soup):
    return "Null"

#Placecode to determine if a level barrier can be found, at the moment returns null for the spreadsheet
def barrier(soup):
    return "Null"

#Placecode to determine if the course is self taught or not, at the moment returns null for the spreadsheet
def selfinstructor(soup):
    return "Null"

#Placecode to determine if the type of learning can be found, at the moment returns null for the spreadsheet
def learningtype(soup):
    return "Null"

#Placecode to determine if the course is in person or it is remote, at the moment returns null for the spreadsheet
def inpersonremote(soup):
    return "Null"


#Placecode to determine if a sites usefulness can be found, at the moment returns null for the spreadsheet
def useful(soup):
    return "Null"

#This is our segment that digs through each sites HTML code to determine our meta data
def main(a):
    #This array is the overall array which will house all meta data tags and the URL
    bigarray = []
    for website in a[0]:
        #This is the array that will be filled with a single URL and metadata tags
        array = []
        try:
            #This semgment is to get each websites HTML code and make it reasonable for the rest of the code to interpret 
            print("starting to scrape", website)
            html = requests.get(website, timeout=5)
            soup = BeautifulSoup(html.content, 'html.parser')
            ###############################
            #This segment finds and appends all meta data tags we are looking for
            array.append(title(soup))
            array.append(website)
            array.append(vendor(soup))
            array.append(cost(soup))
            array.append(publicdod(soup))
            array.append(timecom(soup))
            array.append(certificate(soup))
            array.append(datatopics(soup, a[1]))
            #array.append(a[1])
            #array.append(a[2])
            array.append(languagetype(soup, a[2]))
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
        #These exception requests are the ones we have run into as we have gone on with this project, writen to keep the code running even if one occurs
        except requests.exceptions.SSLError:
            print("\n----------ERROR SSL ERROR----------\n")
        except requests.exceptions.ReadTimeout:
            print("\n----------ERROR TIME OUT ERROR----------\n")
        except requests.exceptions.ConnectionError:
            print("\n----------ERROR CONNECTION ERROR----------\n")
        except TypeError:
            print("\n----------ERROR UNABLE TO READ ERROR----------\n")
    return bigarray



#This is what searches through google itself for every URL used in the crawler
def google():
    #This section generates the search terms will be used
    tuplesearch=searchtermcombo()
    search = '%s %s %s' % (tuplesearch[0],tuplesearch[1],tuplesearch[2])
    print("search terms are:", search)
    x = 0
    urlarrays = []
    #This whileloop goes through pages of google one at a time
    while x <= 100:
        #This segment searches a URL that contains the search terms and what page of google it is looking at
        url = f"https://www.google.com/search?&q={search}&start=" + str(x)
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.text,
                                 "html.parser")
        #Finds all URL's on the page
        heading_object = soup.find_all('a', href=True)
        #This blacklist throws out any url's containing these items as they slow the scrapper down or are unreliable in the long run
        blacklist = ['google','reddit','facebook','pdf']
        #For each url this loop chops off unecessary object that make the url harder to read or illegable to people
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
        #Increase x by 10 for the next page on google, not by 1 that will only go to the next url instead of page
        x += 10
    print("done googling!!!")
    return urlarrays,tuplesearch[0],tuplesearch[1]

#Function to create a spreadsheet based on any array
def sendtospreadsheet(a):
    df = pd.DataFrame(a)
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    writer.save()

#We should delete this
#def test(a):
#    try:
#        soup = bs4.BeautifulSoup(requests.get(a).text, "html.parser")
#        print(soup.prettify())
#       #print(re.findall("\$\d*\.\d\d", soup.prettify()))
#    except requests.exceptions.SSLError:
#        print("does it hit this one?")
#    except requests.exceptions.MissingSchema:
#        print("USnews?????")

#This creates a list of a bunch of URL's, created to determine if specifying certain meta tag lookups would be easier for specific sites or not       
def linklistspredsheet():
    x = 0
    array = []
    while x < 10:
        #Asks for URL's from google
        test = google()
        #Takes a list of all URL's found
        urllist = test[0]
        #Add the searchterms to see what was searched in the list
        searchterms = str(test[1] + ' ' + test[2])
        array.append(str(x) + ' ' + searchterms)
        #Chops the URL into the main part of the site which was the most important for our work at the time
        for url in urllist:
            beg = url.find('://')
            url = url[beg + 3:]
            print(url)
            end = url.find('/')
            url = url[:end]
            array.append(url)
        x += 1
    array.sort()
    sendtospreadsheet(array)

    
if __name__ == '__main__':
    array = main(google())
    #print(array)
    sendtospreadsheet(array)
    #page= metadata_parser.MetadataParser('https://www.coursera.org/learn/python')
    #print(page.metadata)

