from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import traceback

#subjects

subjects = ['Architecture','Art & Culture', 'Biology & Life Sciences', 'Business & Management', 'Chemistry', 'Communication', 'Computer Science', 'Data Analysis & Statistics', 'Design', 'Economics & Finance', 'Education & Teacher Training', 'Electronics', 'Energy & Earth Sciences', 'Engineering', 'Environmental Studies', 'Ethics', 'Food & Nutrition', 'Health & Safety', 'History', 'Humanities', 'Language', 'Law', 'Literature', 'Math', 'Medicine', 'Music', 'Philanthropy', 'Philosophy & Ethics', 'Physics', 'Science', 'Social Sciences']
#subjects = ['Architecture']

#course tab on edx.org
base_website = 'https://www.edx.org/search?tab=course'

#query string as per subject
# eg for Chemistry, https://www.edx.org/search?tab=course&subject=Chemistry
website = 'https://www.edx.org/search?tab=course&subject={courseName}'

# maximum number of courses to parse per subject
MAX_COURSES_PER_SUBJECT = 27

# return url for the passed on subject
def subjectUrl(subName):
    subName = subName.replace(" ","%20").replace("&","%26")
    return website.format(courseName=subName)

## NOTE: Configure WebDriver and append webdriver's location into PATH system variable

# driver = webdriver.Chrome()
driver = webdriver.Edge()

subj = []
title = []
desc = []
weeks = []
hours = []
instit = []
level = []
prereq = []
outcome = []
lang = []
url = []

def isPresent(xpth):
    lst = driver.find_elements( By.XPATH ,xpth)
    if ( len(lst) > 0):
        return lst[0].text
    else:
        return False 

try:
    for subject in subjects:

        #load the subject page
        driver.get(subjectUrl(subject))
        time.sleep(3)

        #Counter cnt
        cnt = 0

        #list of webelements with course links
        course_list_raw = []
        course_list = []

        #do ... while cnt <= MAX_COURSES_PER_SUBJECT and next is enabled
        while(cnt <= MAX_COURSES_PER_SUBJECT):

            iter_list = driver.find_elements(By.XPATH, "/html//main[@id='main-content']/div[@class='new-search-page search-results']/div[3]/div/div[@class='pgn__data-table-layout-wrapper']//div[@class='row']/div[*]/div[@role='group']/a")

            if ( MAX_COURSES_PER_SUBJECT > cnt + len(iter_list) ):
                #Filter out the urls from elements 
                course_list += list(map(lambda x: str(x.get_attribute('href')), iter_list))
                cnt += len(iter_list)

            else:
                #Filter out the urls from elements 
                course_list += list(map(lambda x: str(x.get_attribute('href')), iter_list[:(MAX_COURSES_PER_SUBJECT-cnt)]))
                cnt += MAX_COURSES_PER_SUBJECT-cnt
            
            # NEXT button on course result page
            NEXT_BTN = driver.find_element(By.XPATH,"/html//main[@id='main-content']/div[@class='new-search-page search-results']/div[3]/div//div[@class='pgn__data-table-wrapper']/div[1]/nav/ul[@class='pagination']//button[@class='btn next page-link']")

            # if cnt<MAX_COURSES_PER_SUBJECT and NEXT_BTN is enabled
            if(cnt<MAX_COURSES_PER_SUBJECT and NEXT_BTN.is_enabled()):
                NEXT_BTN.click()
                time.sleep(2)
            else:
                break

        # Subject and count
        print("\nSubject: ", subject)
        print("Count: ",cnt)
        #print(course_list)

        
        for course_page in course_list:

            driver.get(course_page)

            #tit = driver.find_element_by_xpath("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[@class='header']//h1").text
            tit = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[@class='header']//h1")

            des = isPresent("//div[@class='p']")

            wee = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[@class='d-flex flex-column flex-sm-column-reverse']/div[@class='course-snapshot-background']//div[@class='course-snapshot-content py-2 text-primary-500']/div/div[1]/div[@class='ml-3']/div[@class='h4 mb-0']")
            wee = wee.replace('Estimated ','').replace(' weeks', '')

            hou = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[@class='d-flex flex-column flex-sm-column-reverse']/div[@class='course-snapshot-background']//div[@class='course-snapshot-content py-2 text-primary-500']/div/div[1]/div[@class='ml-3']/div[@class='small']")
            hou = hou.replace('hours per week','')

            ins = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[3]//div[@class='row']/div[1]/ul/li[1]")
            ins = ins.replace('Institution: ', '')

            lev = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[3]//div[@class='row']/div[1]/ul/li[3]")
            lev = lev.replace('Level: ', '')

            pre = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[3]/div/div[2]//div[@class='row']/div[1]/ul//*[self::p or self::div]")

            out = driver.find_element(By.XPATH, "/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[3]/div/div[3 or 4]/div[@class='preview-expand-component']/div[2]/div/*").get_attribute('innerHTML')
            
            lan = isPresent("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[3]//div[@class='row']/div[2]/ul/li[1]")
            lan = lan.replace('Language: ','')

            
            #print(tit, des, wee, hou, ins, lev, pre, out, lan, sep='\n')

            if( not(tit and des and wee and hou and ins and lev and pre and lan and len(out)) ):
                continue

            # append values into list
            subj.append(subject)
            title.append(tit)
            desc.append(des)
            weeks.append(wee)
            hours.append(hou)
            instit.append(ins)
            level.append(lev)
            prereq.append(pre)
            outcome.append(out)
            lang.append(lan)
            url.append(course_page)
            
except Exception:
    print('ERROR: Process interupted due to an error at url', driver.current_url)
    print(traceback.format_exc())
    

#closing the browser
driver.close()

df = pd.DataFrame({'subject': subj, 'title': title, 'description': desc, 'weeks': weeks, 'hours': hours, 'institute': instit, 'level':level, 'prerequisites': prereq, 'outcomes': outcome, 'Languages': lang, 'url': url})
df.to_csv('edx-course.csv')
