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
import mysql.connector


def SendEmail(recipients, message, courthouse):
    # Use for attachment:
    #https://levelup.gitconnected.com/send-email-using-python-30fc1f203505
    fromx = "tentativeopinionsbot@gmail.com"
    print(recipients)
    # rec = ""
    # for r in recipients:
    #     rec += r
    #     rec += ","
    # to = rec
    msg = MIMEText(message)
    msg['Subject'] = f'Tentative Opinions for {courthouse}'
    msg['From'] = fromx
    msg['To'] = ", ".join(recipients)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(fromx, "osokfucfyaxdtjnw")
    server.sendmail(fromx, recipients, msg.as_string())
    server.close()


def main():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="tentative_opinions")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.lacourt.org/tentativeRulingNet/ui/main.aspx?casetype=civil")
    courthouse_query = ("SELECT * FROM Courthouse")
    bridge_query = ("SELECT * FROM Email_courthouse WHERE courthouse_id=%s")
    email_query = ("SELECT * FROM Email WHERE email_id=%s")
    mycursor = mydb.cursor(buffered=True)
    # get a list of all of the courthouses
    mycursor.execute(courthouse_query)
    courthouses = []
    for courthouse_id, courthouse_name in mycursor:
        courthouses.append([courthouse_id, courthouse_name])
    for court in courthouses:
        opinion_text = ""
        mycursor.execute(bridge_query, (court[0], ))
        recipients = []
        # for each courthouse, get the recipients
        for emailId, court[0] in mycursor:
            mycursor2 = mydb.cursor(buffered=True)
            mycursor2.execute(email_query, (emailId,))
            for res in mycursor2:
                recipients.append(res[1])
        # get opinion text
        try:
            c1 = driver.find_elements(By.XPATH, f"//*[contains(text(), '{court[1]}')]")
            for c in c1:
                c.click()
                # submit button
                driver.find_element(By.XPATH, "//*[@id='siteMasterHolder_basicBodyHolder_CivilRuling']/tbody/tr/td/div/table[2]/tbody/tr[5]/td[3]/input[1]").click()
                # getting full text of "content text"
                opinion_text += driver.find_element(By.XPATH, "//*[@id='divMainContent']/div/div[3]").text
                opinion_text += "\n"
                opinion_text += "*******************************************"
                opinion_text += "\n"
                # goes to previous page in browser history
                driver.back()
        except NoSuchElementException:
            print("Courthouse does not have any updates")
        SendEmail(recipients, opinion_text, court[1])
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