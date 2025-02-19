import json
from time import sleep
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from sys import argv
import os

from asyncio import run      
               
async def save(numb):
         
          
          if os.path.exists(f"auth_state_{numb }.json"):
               os.remove(f"auth_state_{numb }.json")
          async   with   async_playwright() as p:
         
               browser =await  p.chromium.launch(headless=True)
               co=await browser.new_context()
               page = await co.new_page()
               await page.goto('http://web.bale.ai/login')
              
               await page.fill("div[inputmode='numeric']",numb)
               await page.click("button[aria-label='تایید و ادامه']")
               
               
               codee=input("code")
               
               await page.fill("input[aria-label='text-field-input']",codee)
               cookies = co.cookies()
               sleep(6)
         
               await co.storage_state(path=f"auth_state_{numb}.json")

         
               await browser.close()

   
                    

                    
run(save("989129252158"))
