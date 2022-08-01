from ast import Return
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException        
import smtplib
from email.mime.text import MIMEText
from datetime import date


def SendEmail(recipients, message):
    # Use for attachment:
    #https://levelup.gitconnected.com/send-email-using-python-30fc1f203505

    fromx = "tentativeopinionsbot@gmail.com"
    to = recipients
    msg = MIMEText(message)
    msg['Subject'] = f'Tentative Opinions for {date.today()}'
    msg['From'] = fromx
    msg['To'] = to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(fromx, "osokfucfyaxdtjnw")
    server.sendmail(fromx, to, msg.as_string())
    server.close()


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.lacourt.org/tentativeRulingNet/ui/main.aspx?casetype=civil")
    # gets a list of all of the matching options
    opinion_text = ""
    try:
        c1 = driver.find_elements(By.XPATH, "//*[contains(text(), 'Alhambra Courthouse:  Dept. 3')]")
        for c in c1:
            c.click()
            # submit button
            driver.find_element(By.XPATH, "//*[@id='siteMasterHolder_basicBodyHolder_CivilRuling']/tbody/tr/td/div/table[2]/tbody/tr[5]/td[3]/input[1]").click()
            # getting full text of "content text"
            opinion_text += driver.find_element(By.XPATH, "//*[@id='divMainContent']/div/div[3]").text
            # print(opinion_text)
            # print("*************END OF TEXT**************")
            # goes to previous page in browser history
            driver.back()
    except NoSuchElementException:
        print("Courthouse does not have any updates")
    SendEmail("syerragu@usc.edu", opinion_text)
    driver.close()

main()






# selects the Choice 2 table
# courthouse_table = Select(driver.find_element(By.ID, 'siteMasterHolder_basicBodyHolder_List2DeptDate'))
# first courthouse in the table
# courthouse_table.select_by_value('ALH,3,07/14/2022')


## Getting as HTML file ###
# page = driver.page_source.encode('utf-8')
# file_ = open('result.html', 'wb')
# # Write the entire page content in result.html
# file_.write(page)
# # Closing the file
# file_.close()
# # Closing the driver
# driver.close()