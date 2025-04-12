import json
from time import sleep
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from sys import argv
import os

from asyncio import run      
               
async def save(ctr,numb):
         
          
          
          async   with   async_playwright() as p:
               if os.path.exists(f"auth_state_{numb }.json"):
                    os.remove(f"auth_state_{numb }.json")
               browser =await  p.chromium.launch(headless=False)
               co=await browser.new_context()
               page = await co.new_page()
               
               await page.goto('https://web.bale.ai/fa/login')
               await page.wait_for_load_state("networkidle")
               # await page.status
               await page.locator("button[aria-label='Got it']").click(force=True)
               
               await page.locator("button[aria-label='Login']").click(force=True)
              
               
               
               
               await page.fill("input[inputmode='numeric']",numb)
               await page.click("button[aria-label='Submit and Continue']")
               
               
               codee=input("code")
               
               await page.fill("input[aria-label='text-field-input']",codee)
               cookies = co.cookies()
               sleep(6)
         
               await co.storage_state(path=f"auth_state_{numb}.json")

         
               await browser.close()
run(save("Iran","9129252158"))
   
                    

                    

