import os
from time import sleep
from turtle import down
from bs4 import BeautifulSoup
from fastapi import FastAPI
from playwright.async_api import async_playwright
from asyncio import run, sleep as async_sp
import requests
import asyncio



async def getvideo(num, chlist):
            p=await async_playwright().start()
            vidoeslist=[]
            browser = await p.chromium.launch(headless=False, timeout=50000)
            context = await browser.new_context(
            storage_state=f"auth_state_{num}.json",accept_downloads=True,ignore_https_errors=True)
            # context.set_download_behaviour
            
            result = {}
            
            for chname in chlist:
               os.makedirs(chname,exist_ok=True)
             
               download_path = f"{chname}/Videos/"
            #    def handle_download(download):
            #         # Specify your folder path here
            #        download.save_as(download_path + "/" + download.suggested_filename)

            #    context.on('download', handle_download)
               page = await context.new_page()
            #    await page.ex
               churl = f"https://web.bale.ai/@{chname}"
                
               await page.goto(churl)
               await page.wait_for_load_state("networkidle")
               content= page.locator("div.content")
               await content.click()
                # while True:
               videoloc=page.query_selector_all("video.media-video")
                # print(await videoloc);import pdb; pdb.set_trace()
               for v in await videoloc:
                  
                    async with page.expect_download() as download_info:
                        await v.wait_for_element_state(state="stable")
                        await v.click()
                        await page.wait_for_selector("button.btn-icon.tgico-download")
    # Perform the action that initiates download
    # await page.get_by_text("Download file").click()
                        
                        downloc=page.locator("button.btn-icon.tgico-download")
                        await downloc.click(force=True)
                        download = await download_info.value  # This will give you the download object
                        print(f"Download started: {download.suggested_filename}")
                        
                        await download.save_as(download_path + download.suggested_filename)
                            
                            
                    
                        sleep(1)
                        mediaviewerloc=page.locator("div.media-viewer-topbar.media-viewer-appear")
                        await mediaviewerloc.wait_for(state='visible')
                        # await page.goto(churl,wait_until="networkidle")
                        closeloc=mediaviewerloc.locator("button.btn-icon.tgico-close").last
                        sleep(0.5)
                        
                        await closeloc.wait_for(state='visible')        
                        await closeloc.click(force=True)
                    # span = await page.query_selector('span.video-time')

                    # if span:
                    #     # Check if the text content is 'GIF'
                    #     text_content = await span.text_content()
                    #     if text_content and text_content.strip() == "GIF":
                    #         print("Found a span with class 'video-time' and text 'GIF'")
                    #     else:
                    #         print("Found a span with class 'video-time' but text is not 'GIF'")
                    # else:
                    #     print("No span with class 'video-time' found")

                    # async_sp(1)
                    
                    
            await browser.close()

                
                        
                        