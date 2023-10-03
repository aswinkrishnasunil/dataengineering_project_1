
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#option = webdriver.ChromeOptions()
#option.add_argument("start-maximized")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://edition.cnn.com/markets?utm_source=business_ribbon')

title = driver.title
eles=driver.find_elements(By.XPATH,'//a[@class="basic-table__link-1GsgPj cnn-pcl-12a2lqo"]')

#print(eles.text)
#driver.quit()    
mylist=[]
for a_element in eles:
        element_text = a_element.text
        if element_text in ['Dow Index','NASDAQ Index','S&P 500 Index']:
                continue
        mylist.append(element_text)
        
print (mylist)

# Don't forget to close the WebDriver when you're done
driver.quit()


driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


#title1 = driver.title
#print(title1)
pc=[]
op=[]
for query in mylist:
        driver1.get('https://finance.yahoo.com/quote/PFE?p=PFE&.tsrc=fin-srch')
        search_element = driver1.find_element(By.XPATH,'//*[@id="yfin-usr-qry"]')
        search_element.clear()
        WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yfin-usr-qry"]')))

        search_element.send_keys(query)

        search_element.send_keys(Keys.ENTER)

        

        eles1=driver1.find_element(By.XPATH,'//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]')
        a=eles1.text
        #print("pc",query,"=" ,a)
        eles2=driver1.find_element(By.XPATH,'//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]')
        b=eles2.text
        #print("op",query,"=" ,b)
        pc.append(a)
        op.append(b)
        


print(pc)  
print(op)      
driver1.quit()
