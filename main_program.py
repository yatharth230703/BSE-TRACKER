######retriver me file path jabhi jaega jab href usse match KAREGA , cause href value most recent wali hai 
import re
from retriever_package import retriever
import os
from msgerwhatsapp import whtsapp_sender
from screener import get_financials, get_yr_reven
from complete_download import pdf_scraper
from sheets_upload import sheets_updater
from if_order_0 import if_zero
from is_legal import legality
#from new_msgr import whtsapp
from current_time import is_time_in_range_ist

import shutil
import time
from datetime import datetime, timedelta
while(True):    
    row=[]
    script_dir=os.path.dirname(os.path.abspath(__file__))
    
    main_dir = os.path.join(script_dir, "pdf_Store")
    ##reciever company, reciever ID , order date time , pdf link from final_final_pdf_Scraper
    ## order recieved from ,order value, execution period from retriever 
    ##quaterly revenue , quaterly profit from screener 
    title =""
    date_time=""
    pdflink=""
    print("calling pdf scraper ")
    title, date_time , pdflink ,breaker=  pdf_scraper(0)
    print("scraper called")
    if(breaker==1):
        continue
    
    def extract_filename_from_url(url):
        filename = url.split('/')[-1]
        return filename
    f=extract_filename_from_url(pdflink)
    pdf_dir = os.path.join(main_dir,f)
    
    def extract_company_details(title):
        # Use regex to find the pattern for company ID and name
        match = re.match(r'^(.*?)\s-\s(\d+)\s-', title)
        
        if match:
            company_name = match.group(1)  # Group 1 is the company name
            company_id = match.group(2)    # Group 2 is the company ID
            return company_name.strip(), company_id.strip()
        else:
            return "***", "***"
    islegal=legality(pdf_dir)
    islegal=str(islegal)
    print(type(islegal))
    legalflag=""
    if("y" in islegal.lower()):
        print("islegal")
        legalflag="Legal"
    else:
        legalflag="New Order"
    reciever_comp , compID = extract_company_details(title)
    reciever_comp=str(reciever_comp)
    compID=str(compID)
    date_time=str(date_time)
    row.append(reciever_comp)
    row.append(compID)
    row.append(date_time)
    #row.append(pdflink)

    print("calling retriever ")
    order_sender , order_val , exec_prd = retriever(pdf_dir)
    print("retriever called")
    
    order_val=str(order_val)
    order_sender=str(order_sender)
    exec_prd=str(exec_prd)
    row.append(order_val)
    row.append(order_sender)
    row.append(exec_prd)
    print("fetching screener reports")
    reven , proft ,mcap , spe= get_financials(compID)
    print("recieved reports ")
    yreven = get_yr_reven(compID)
    
    reven=str(reven)
    proft=str(proft)
    mcap=str(mcap)
    spe=str(spe)
    yreven=str(yreven)
    
    #pdflink=str(pdflink)
    row.append(reven)
    row.append(proft)
    row.append(mcap)
    row.append(spe)
    row.append(yreven)

    row.append(pdflink)
    row.append(legalflag)
    
    msg = f"""
    ****************
    New Order!
    Reciever Name : {reciever_comp}
    Order Type: {legalflag}
    Time of Arrival : {date_time}

    Link to pdf : {pdflink}

    Order Value : {order_val}

    Order Recieved from: {order_sender}

    Execution Period : {exec_prd}

    Revenue Last Quarter : {reven}

    Profit Last Quarter : {proft}
    
    Market Cap : {mcap}
    
    Stock PE : {spe}
    
    Yearly Revenue : {yreven}

    """
    
    whtsapp_sender(msg)
    
    sheets_updater(row)

    def delete_contents(directory):
        """
        Delete all contents of the specified directory.
        """
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    
    if (is_time_in_range_ist("23:55" , "00:05")):
        delete_contents(main_dir)
    
    
    

    
