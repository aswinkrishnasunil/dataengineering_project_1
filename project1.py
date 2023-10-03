
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
