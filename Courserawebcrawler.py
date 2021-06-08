from selenium import webdriver
import time
import pandas as pd
import xlsxwriter
from selenium.webdriver.chrome.options import Options



languages = ['Python', 'Java', 'Matlab', 'R ', 'C ', 'C++ ', 'Julia', 'Labview', 'SAS', 'COMSOL']


def coursera(search):
    x = 1
    urlarrays = []
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    window_before = ""
    #Download chromedriver and add it to your project, then copy the path to it below instead of mine
    browser = webdriver.Chrome(executable_path='/Users/DuncanBishop/PycharmProjects/Courseracrawler/chromedriver', options=chrome_options)
    #This whileloop goes through pages of coursera one at a time
    while x <= 10:
        print(x)
        url = f"https://www.coursera.org/search?query={search}&page={x}&index=prod_all_products_term_optimization&allLanguages=English"
        browser.get(url)
        windoworigin = browser.window_handles[0]
        browser.switch_to.window(windoworigin)
        time.sleep(5)
        print(url)
        items = browser.find_elements_by_xpath('//li[@class="ais-InfiniteHits-item"]')
        for p in range(len(items)):
            splititems = items[p].text
            splititems = splititems.split('\n')
            urlarrays.append(splititems)
        for test in items:
            test.click()
        browser.switch_to.window(windoworigin)
        handles = browser.window_handles
        handles.pop(0)
        numberurl = -1
        for windows in handles:
            browser.switch_to.window(windows)
            hours = browser.find_elements_by_xpath("//*[text()[contains(.,'Suggested pace')]]")
            if len(hours) == 2:
                hours = hours[1].text
                hours = hours[18:]
            elif len(hours) == 1:
                hours = hours[0].text
                hours = hours[18:]
            else:
                hours = browser.find_elements_by_xpath("//*[text()[contains(.,'Approx')]]")
                if len(hours) == 2:
                    hours = hours[1].text
                    hours = hours[8:10]
                elif len(hours) == 1:
                    hours = hours[0].text
                    hours = hours[8:10]
                else:
                    hours = browser.find_elements_by_xpath("//*[text()[contains(.,'minutes')]]")
                    if hours != None:
                        hours = "<1"
                    else:
                        hours = "Null"
            tags = browser.find_elements_by_xpath('//span[@class="_rsc0bd m-r-1s m-b-1s"]')
            tagsarray = []
            for tag in tags:
                tagsarray.append(tag.text)
            Typecourse = browser.find_elements_by_xpath("//*[text()[contains(.,'Course Videos & Readings')]]")
            if Typecourse != None:
                urlarrays[numberurl].append(True)
            else:
                urlarrays[numberurl].append(False)
            urlarrays[numberurl].append(tagsarray)
            urlarrays[numberurl].append(hours)
            urlarrays[numberurl].append(browser.current_url)
            numberurl -= 1
        handles = browser.window_handles
        for windows2 in handles:
            browser.switch_to.window(windows2)
            sizeof = browser.window_handles
            if(len(sizeof) > 1):
                browser.close()
        x += 1
    print(urlarrays)
    return urlarrays

def compilelist(array):
    newarray = []
    for i in array:
        languageused = ""
        testarray = []
        testarray.append(i[0])
        testarray.append(i[-1])
        testarray.append(i[1])
        testarray.append("$399 (Yearly)") #Cost
        testarray.append("Public")
        testarray.append(i[-2])
        if "CERTIFICATE" in i[2] or "Certificate" in i[2]:
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
        testarray.append("California") #Base of operations
        testarray.append(i[-5])
        testarray.append("Self Paced")
        if i[-4] == True:
            testarray.append("Recorded Video and Text Tutorials")
        else:
            testarray.append("Null")
        testarray.append("Remote")
        if "GUIDED" in i[3]:
            testarray.append(i[4])
        elif "Rated" not in i[3]:
            testarray.append("Null")
        else:
            testarray.append(i[3]) #Useful
        testarray.append("Null") #Comments
        newarray.append(testarray)
    print(newarray)
    return newarray

def sendtospreadsheet(a):
    df = pd.DataFrame(a)
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    writer.save()


if __name__ == '__main__':
    searchterm = "Python"
    searchterm = searchterm.replace(" ", "%20")
    array = coursera(searchterm)
    bigarray = compilelist(array)
    sendtospreadsheet(bigarray)
 
