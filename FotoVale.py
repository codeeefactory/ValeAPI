from time import sleep
from bs4 import BeautifulSoup
from fastapi import FastAPI
from ldap3 import ASYNC
from playwright.async_api import async_playwright
import os
from asyncio import run, sleep as async_sp
import requests
import asyncio

async def download_image(img_url: str, filename: str):
    
    print(f"Downloading photo from {img_url}...")
    response = requests.get(img_url, stream=True)
    
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
            f.write(chunk)
    print(f"Downloaded the image to {filename}.")
async def getphoto(num, chlist):
            p=await async_playwright().start()
            vidoeslist=[]
            browser = await p.chromium.launch(headless=False, timeout=50000)
            context = await browser.new_context(
            storage_state=f"auth_state_{num}.json",accept_downloads=True)
            result = {}
            page = await context.new_page()
            for chname in chlist:
                os.makedirs(chname,exist_ok=True)
                os.path.join(os.getcwd(),chname)
             
                download_path = f"{chname}/"
                
                churl = f"https://web.bale.ai/@{chname}"
                await page.goto(churl)
                await page.wait_for_load_state("networkidle")
                # content= page.locator("div.content")
                # await content.click()
                medialoc=page.query_selector_all("img[alt='Photo Message']")
                # photoloc=page.query_selector_all(".img.media-photo");import pdb; pdb.set_trace()
                # print(await photoloc);import pdb; pdb.set_trace()
                for f in await medialoc:
                    
                            sleep(1)
                            print(await f.get_attribute("src"))
                            src = await f.get_attribute("src")

                            os.system(f"""wget --output-document={chname}/{src}.jpeg "{src}" """)
                            await page.evaluate("""
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
        """)
        
        # Wait for the image element to be visible (adjust the selector as needed)
                            await page.wait_for_selector("img", state="visible")
                            # sleep(2)
        # Perform the action that initiates download
        # await page.get_by_text("Download file").click()
                            
                       
            # Create a directory to save images if it doesn't exist
            # os.makedirs(chname, exist_ok=True)
            # os.makedirs(f"photos_{chname}", exist_ok=True)
            

            
            # for idx, img_src in enumerate(vidoeslist, start=1):
            #     if img_src:
            #         # Generate a filename for each image
            #         page2=await context.new_page()
            #         image_folder = os.path.join(chname,f"photos_{chname}")
            #         # image_filename = os.path.join(image_folder, f"{idx}.jpg")
            #         await page2.goto(img_src)
                    
            #         await page.wait_for_load_state("networkidle")
            #         await page2.screenshot(type='jpeg',path=image_folder)
                    
            #         # Download the image
run(getphoto("9129252158",["varzesh3"]))