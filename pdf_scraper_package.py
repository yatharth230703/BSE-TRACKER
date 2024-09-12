import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def pdf_scraper(breaker):
    title = ""
    dtime = ""
    pdflink = ""
    breaker = 0
    script_dir=os.path.dirname(os.path.abspath(__file__))
    
    download_directory = os.path.join(script_dir, "pdf_Store")
    os.makedirs(download_directory, exist_ok=True)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.bseindia.com/corporates/ann.html")
    time.sleep(3)

    try:
        # Select the category and subcategory
        category_dropdown = Select(driver.find_element(By.ID, "ddlPeriod"))
    except Exception as e:
        driver.quit()
        return "*", "*", "*", 1

    try:
        category_dropdown.select_by_visible_text("Company Update")
        time.sleep(2)
        subcategory_dropdown = Select(driver.find_element(By.ID, "ddlsubcat"))
    except Exception as e:
        driver.quit()
        return "*", "*", "*", 1

    try:
        subcategory_dropdown.select_by_visible_text("Award of Order / Receipt of Order")
        time.sleep(2)
        submit_button = driver.find_element(By.ID, "btnSubmit")
    except Exception as e:
        driver.quit()
        return "*", "*", "*", 1

    try:
        submit_button.click()
        time.sleep(5)
    except Exception as e:
        driver.quit()
        return "*", "*", "*", 1

    # Function to scroll down the page
    def scroll_down(driver, pixels):
        driver.execute_script(f"window.scrollBy(0, {pixels});")
    scroll_down(driver, 300)
    time.sleep(3)
    
    # Function to wait for downloads to finish
    def wait_for_downloads(directory):
        while any(filename.endswith('.tmp') or filename.endswith('.crdownload') for filename in os.listdir(directory)):
            time.sleep(1)

    # Helper function to check if a PDF file matching the href already exists
    def pdf_exists_in_directory(href, directory):
        # Extract the PDF filename from the href (assuming it's the last part after the last '/')
        pdf_filename = href.split('/')[-1]
        # List all PDF files in the directory
        existing_files = os.listdir(directory)
        # Check if any existing file matches the expected PDF filename
        return any(pdf_filename in filename for filename in existing_files if filename.endswith('.pdf'))


    i = 1
    while True:
        try:
            xpath = "//*[@id='lblann']/table/tbody/tr[4]/td/table[" + str(i) + "]/tbody/tr[1]/td[4]/a"
            xpath_heading = "/html/body/div[1]/div[5]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[" + str(i) + "]/tbody/tr[1]/td[1]/span"
            xpath_time = "/html/body/div[1]/div[5]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/table[" + str(i) + "]/tbody/tr[3]/td/b[1]"
            
            
            element = driver.find_element(By.XPATH, xpath)


            href = element.get_attribute("href")
            
            # Check if the PDF already exists in the download directory
            if pdf_exists_in_directory(href, download_directory):
                i += 1
                print("PDF already exists in the directory. Skipping...")
                scroll_down(driver, pixels=200)
                time.sleep(1)
                continue  # Skip to the next element if the PDF is already downloaded
            print("NEW PDF FOUND!!!!!!!!!!!!!")
            # If the PDF does not exist, continue with your block
            heading = driver.find_element(By.XPATH, xpath_heading)
            timing = driver.find_element(By.XPATH, xpath_time)
     

            title = heading.get_attribute("innerText")
            pdflink = href
            dtime = timing.get_attribute("innerText")
            
            element.click()
            time.sleep(3)
            wait_for_downloads(download_directory)
            scroll_down(driver, pixels=200)
            i += 1
            #driver.quit()
            breaker=0
            break
        except Exception as e:
            print(f"No more links found. Last table index: {i - 1}")
            breaker = 1
            break
    
    driver.quit()

    def delete_temp_files(directory):
        #Get a list of all files in the directory
        files_in_directory = os.listdir(directory)
        
        # Loop through each file in the directory
        for file_name in files_in_directory:
            # Check if the file ends with .tmp or .crdownload
            if file_name.endswith('.tmp') or file_name.endswith('.crdownload'):
                # Construct the full file path
                file_path = os.path.join(directory, file_name)
                try:
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    delete_temp_files(download_directory)
    return title, dtime, pdflink, breaker



#a,b,c,d = pdf_scraper(0)
#print(a,"\n",b,"\n",c,"\n",d)