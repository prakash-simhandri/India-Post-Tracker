from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time,json,requests

tracking_number = input("Enter Your Tracking Number ")
mobile_number = input(" Enter your mobile number")
flag = True
def post_tracker():
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://trackcourier.io/speed-post-tracking")
    driver.maximize_window()
    driver.find_element_by_xpath("/html/body/div/div/div/div[1]/fieldset/form/div[1]/input").send_keys(tracking_number)
    driver.find_element_by_xpath("/html/body/div/div/div/div[1]/fieldset/form/div[2]/button[1]").click()
    time.sleep(5)
    select = Select(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[2]/select"))
    select.select_by_visible_text('India Post Domestic')
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/div[3]/button").click()
    time.sleep(5)
    page = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(page,"html.parser")
    data = soup.findAll('li', class_="checkpoint ng-scope")
    Events_list =[]
    for list in data:
        Event_Details = {}
        date_time = list.find('div',class_="checkpoint__time").text.split()
        Event_Details["date"]=date_time[0]
        Event_Details["time"]=date_time[1]
        spliter = list.find('span',class_="ng-binding").text
        spliter_done = ''
        for i in spliter:
            if i!= "\u20b9":
                spliter_done+=i
        Event_Details['event']=spliter_done
        Office=list.find('div',class_="checkpoint__content")
        Event_Details["office"]=Office.find('div',class_="hint ng-binding").text
        Events_list.append(Event_Details)
    with open('tracker1.json','w+') as write_data:
        json.dump(Events_list,write_data)
    with open('tracker1.json','r') as write_data:
        reader1 =json.load(write_data)
        with open('tracker.json','r') as read_data:
            reader = json.load(read_data)
            if flag:
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message="+str(Events_list)+"&language=english&route=p&numbers="+mobile_number    
                headers = {
                'authorization': "SbGBWXK9CcnHRdUsex0w72hoyAFQZrYzNfIEu354vPkmJ1La8tN9L7UoAWgiaBMuY13bkrQRxSclOyfV",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text)
                flag = False
            else:
                if len(reader) < len(reader1):
                    url = "https://www.fast2sms.com/dev/bulk"
                    payload = "sender_id=FSTSMS&message="+str(Events_list[0])+"&language=english&route=p&numbers=9566669186"      
                    headers = {
                    'authorization': "SbGBWXK9CcnHRdUsex0w72hoyAFQZrYzNfIEu354vPkmJ1La8tN9L7UoAWgiaBMuY13bkrQRxSclOyfV",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache",
                    }
                    response = requests.request("POST", url, data=payload, headers=headers)
                    print(response.text)

                    with open('tracker.json','w+') as data_file:
                        json.dump(Events_list,data_file)
    driver.quit()
    time.sleep(28800)
    post_tracker()
post_tracker()
