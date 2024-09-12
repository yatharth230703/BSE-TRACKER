from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import time

def get_financials(bse_id):
   
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        website = "https://www.screener.in/company/" + bse_id + "/#quarters"
        driver.get(website)
        
        time.sleep(3)
        
        rev_xpath = '//*[@id="quarters"]//table/tbody/tr[1]/td[position()=last()]'
        
      
        r = driver.find_element(By.XPATH, rev_xpath)
        a = r.get_attribute("innerText")
        
        netp_xpath = '//*[@id="quarters"]//table/tbody/tr[10]/td[position()=last()]'
        
        p = driver.find_element(By.XPATH, netp_xpath)
        b = p.get_attribute("innerText")
        
        market_cap ="//ul/li[1]/span[2]"
        m = driver.find_element(By.XPATH , market_cap)
        mc=m.get_attribute("innerText")
        
        stock_pe="/html/body/main/div[3]/div[3]/div[2]/ul/li[4]/span[2]/span"
        
        s=driver.find_element(By.XPATH, stock_pe)
        sp=s.get_attribute("innerText")
        
        #find out table size by for loop and then search for element 
        

        
        print("Current URL after search:", driver.current_url)
        return a, b , mc,sp
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "**", "**","**","**","**"
    
    finally:
        driver.quit()
        
def get_yr_reven(bse_id):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        website = "https://www.screener.in/company/" + bse_id + "/#profit-loss"
        driver.get(website)
        
        time.sleep(3)
        yr_reven='//*[@id="profit-loss"]//table/tbody/tr[1]/td[position()=last()-1]'
        
        
        #/html/body/main/section[5]/div[2]/table/tbody/tr[1]
       # /html/body/main/section[5]/div[3]/table/tbody/tr[1]/td[11]
       
    
        y=driver.find_element(By.XPATH, yr_reven)
        yr=y.get_attribute("innerText")
        return yr

    except Exception as e:
        print(f"An error occurred: {e}")
        return "**"
    
    finally:
        driver.quit()

#a,b,c,d=get_financials("539876")
#print(a,b,c,d)





















































