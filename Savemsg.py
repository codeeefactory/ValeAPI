from time import ctime
from bs4 import BeautifulSoup
from fastapi import FastAPI
from playwright.async_api import async_playwright
from asyncio import run, sleep as async_sleep
from typing import List
import asyncio
from ValeDB import Channel, Message, MongoDB
from datetime import datetime

async def slow_scroll_to_bottom(page, step=100, delay=0.1):
   
    last_height = await page.evaluate("document.body.scrollHeight")
    current_position = 0

    while current_position < last_height:
        current_position += step
        await page.evaluate(f"window.scrollTo(0, {current_position})")
        await asyncio.sleep(delay)
        last_height = await page.evaluate("document.body.scrollHeight")


async def getmsgs(join_list):
    mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="Vale")
    p=await async_playwright().start()
    counter_types=[]
    counter_values=[]
    
    browser = await p.chromium.launch(headless=False, timeout=50000)
    # context = await browser.new_context(
    #     storage_state=f"auth_state_{num}.json")
    result = {}

    for chname in join_list:
        page = await browser.new_page()
        churl = f"https://ble.ir/{chname}"
        
        await page.goto(churl)
        
        await page.wait_for_load_state("networkidle")
        last_seen_message = None
        
        soup = BeautifulSoup(await page.content(), features="html.parser")
        name = soup.find("h1", {
            "class": "Profile_name__pQglx"
        }).text
        biogsel=page.locator("div.Profile_description__YTAr_")
        biog = biogsel.locator("div.Text_text__7_UOM")
        membercount=soup.find("div", {
            "class": "Profile_peer-count__WofG1"
        }).text
       
        # msgloc=soup.find_all("span",class_="p")

        # previously_extracted = set()
        # previously_extracted.update([x for x in msgloc])
        # previously_extracted2 = set()
        # previously_extracted2.update([x.text for x in msgloc])
        print(name)
        bio= biog.locator("span.p")   

        bioglist=[x for x in await bio.all_text_contents()]
        

        print(bioglist)
        print(membercount)

        while True:


            await page.evaluate("window.scrollTo(0, 0)")

            await asyncio.sleep(2)

            new_content = await page.content()
            # soup = BeautifulSoup(new_content, "html.parser")
            soup = BeautifulSoup(new_content, 'html.parser')

# Find the div with the specific class
            msgdiv = page.locator("div[class='Text_text__0QjN9TextMessage_text__ADtXW']")
            msgtxt=msgdiv.locator("span.p")
            photocapdiv = page.locator("div[class='Text_text__7_UOM Photo_caption__uXXa5']")
            captxt=photocapdiv.locator("span.p")
            span_texts = [[span for span in await msgtxt.all_text_contents()]+ [photocap for photocap in await captxt.all_text_contents()]]
            print(span_texts)


            msgins = Message(username=chname,
                                link=f"https://ble.ir/{chname}/{element_locator}",
                                text=span_texts,crawldate=ctime())
            await mongo_db.save_message(msgins)
          
            chins=Channel(channel_name=name,bio=biog,username=f"@{chname}",counter_type= counter_types,counter_value=counter_values)
            await mongo_db.save_channel(chins)

    await browser.close()
