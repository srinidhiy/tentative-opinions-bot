from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.lacourt.org/tentativeRulingNet/ui/main.aspx?casetype=civil")

# selects the Choice 2 table
courthouse_table = Select(driver.find_element(By.ID, 'siteMasterHolder_basicBodyHolder_List2DeptDate'))
# first courthouse in the table
courthouse_table.select_by_value('ALH,3,07/14/2022')
# submit button
driver.find_element(By.XPATH, "//*[@id='siteMasterHolder_basicBodyHolder_CivilRuling']/tbody/tr/td/div/table[2]/tbody/tr[5]/td[3]/input[1]").click()
# getting full text of "content text"
opinion_text = driver.find_element(By.XPATH, "//*[@id='divMainContent']/div/div[3]").text

driver.close()




## Getting as HTML file ###
# page = driver.page_source.encode('utf-8')
# file_ = open('result.html', 'wb')
# # Write the entire page content in result.html
# file_.write(page)
# # Closing the file
# file_.close()
# # Closing the driver
# driver.close()