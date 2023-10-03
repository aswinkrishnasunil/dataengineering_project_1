
import csv
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
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
v=[]
op=[]
pe=[]
for query in mylist:
        driver1.get('https://finance.yahoo.com/quote/PFE?p=PFE&.tsrc=fin-srch')
        search_element = driver1.find_element(By.XPATH,'//*[@id="yfin-usr-qry"]')
        search_element.clear()
        WebDriverWait(driver1, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yfin-usr-qry"]')))

        search_element.send_keys(query)

        time.sleep(3)

        search_element.send_keys(Keys.ENTER)

        try:

                eles1=driver1.find_element(By.XPATH,'//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/fin-streamer')
                a=eles1.text
                print("v",query,"=" ,a)
                eles2=driver1.find_element(By.XPATH,'//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]')
                b=eles2.text
                print("op",query,"=" ,b)
                eles3=driver1.find_element(By.XPATH,'//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]')
                c=eles3.text
                print("pe",query,"=" ,c)
                print("..................")
        except:
              a=0
              b=0
              c=0
              print(a)
              print(b)
              print(c)
        v.append(a)
        op.append(b)
        pe.append(c)
        

print("volume")
print(v)  
print("open")
print(op) 
print("pe ratio")
print(pe)     
driver1.quit()


#csv_file = open('project1.csv','w')          #'w' - methode used to write data to a file
#csv_writer = csv.writer(csv_file) 
#csv_writer.writerow(['symbols','open','volume','PE RATIO'])
csv_file_name='project1.csv'

      
try:
        dict = {'symbols':mylist,'open':op,'volume':v,'PE RATIO':pe}
        df = pd.DataFrame(dict)
except:
        print("data not updated to dictionary")

print(df)
df.to_csv(csv_file_name, index=False)

def create_database():
    try:
        conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=password")
    except psycopg2.Error as e :
        print("error,couldnt conmnect to database")
        print(e)
    conn.set_session(autocommit=True) 
    #sets the database connection's session to autocommit mode. In autocommit mode, each SQL statement you execute is automatically committed to the database
    cur = conn.cursor()
    # the cur cursor to execute SQL statements and queries within an autocommit mode, and the changes will be immediately applied to the database without the need for explicit commit commands.
    
    cur.execute("DROP DATABASE IF EXISTS project1")#drop the database "movie" if it exists
    cur.execute("CREATE DATABASE project1")  #creating a new database named"movie"
    
    #close connection to default database
    conn.close()
    try:
        conn = psycopg2.connect("host=localhost dbname=project1 user=postgres password=password")
    except psycopg2.Error as e:
        print("error, couldnt connect to database")
        print(e)
    conn.set_session(autocommit = True)    
    cur = conn.cursor()
    
    return cur , conn



cur , conn = create_database()

tab= (""" CREATE TABLE  one(
symbols VARCHAR PRIMARY KEY,
open VARCHAR ,
volume VARCHAR,
PE_RATIO VARCHAR) """)

cur.execute(tab)
conn.commit()

tab_insert = (""" insert into one(symbols,open,volume,PE_RATIO)
values(%s,%s,%s,%s)""")

for i,row in df.iterrows():# iterrows returns index and information stored in a row of a data frame
    cur.execute(tab_insert,list(row))