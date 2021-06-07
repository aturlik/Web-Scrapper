from selenium import webdriver
import time
import pandas as pd
import xlsxwriter

languages = ['Python', 'Java', 'Matlab', 'R ', 'C ', 'C++ ', 'Julia', 'Labview', 'SAS', 'COMSOL']


def coursera(search):
    x = 1
    urlarrays = []
    #Download chromedriver and add it to your project, then copy the path to it below instead of mine
    browser = webdriver.Chrome(executable_path='/Users/DuncanBishop/PycharmProjects/Courseracrawler/chromedriver')
    #This whileloop goes through pages of coursera one at a time
    while x <= 1:
        url = f"https://www.coursera.org/search?query={search}&page={x}&index=prod_all_products_term_optimization&allLanguages=English"
        browser.get(url)
        time.sleep(1)
        items = browser.find_elements_by_xpath('//li[@class="ais-InfiniteHits-item"]')
        for p in range(len(items)):
            splititems = items[p].text
            splititems = splititems.split('\n')
            urlarrays.append(splititems)
        for test in items:
            test.click()
        x += 1
    handles = browser.window_handles
    handles.pop(0)
    numberurl = -1
    for windows in handles:
        browser.switch_to_window(windows)
        hours = browser.find_elements_by_xpath("//*[text()[contains(.,'Approx')]]")
        hours = hours[1].text
        tags = browser.find_elements_by_xpath('//span[@class="_rsc0bd m-r-1s m-b-1s"]')
        tagsarray = []
        for tag in tags:
            tagsarray.append(tag.text)
        urlarrays[numberurl].append(tagsarray)
        urlarrays[numberurl].append(hours)
        urlarrays[numberurl].append(browser.current_url)
        numberurl -= 1
    return urlarrays

def compilelist(array):
    newarray = []
    for i in array:
        languageused = ""
        testarray = []
        testarray.append(i[0])
        testarray.append(i[-1])
        testarray.append(i[1])
        testarray.append("Null")
        testarray.append("Public")
        testarray.append(i[-2])
        if "PROFESSIONAL CERTIFICATE" == i[2]:
            testarray.append("Yes")
        else:
            testarray.append("No")
        testarray.append(i[-3])
        for L in languages:
            if L in i[0]:
                if languageused == "":
                    languageused += L
                else:
                    languageused = languageused + " and " + L
        testarray.append(languageused)
        testarray.append("Null")
        testarray.append(i[-4])
        testarray.append("Null")
        testarray.append("Null")
        testarray.append("Remote")
        testarray.append("Null")
        testarray.append("Null")
        newarray.append(testarray)
    return newarray

def sendtospreadsheet(a):
    df = pd.DataFrame(a)
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    writer.save()

if __name__ == '__main__':
    searchterm = "Python"
    array = coursera(searchterm)
    bigarray = compilelist(array)
    sendtospreadsheet(bigarray)
    #print(array)
    #sendtospreadsheet(array)
    #page= metadata_parser.MetadataParser('https://www.coursera.org/learn/python')
    #print(page.metadata)
