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
    mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="eitaa")
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
        biog = soup.find("div", {
            "class": "Text_text__7_UOM"
        }).text
        membercount=soup.find("div", {
            "class": "Profile_peer-count__WofG1"
        }).text
       
        msgloc = soup.find_all("div", attrs={"data-post": True})
        txtloc = soup.find_all(
            "div", class_={"Text_text__0QjN9 TextMessage_text__ADtXW"})

        previously_extracted = set()
        previously_extracted.update([x for x in msgloc])
        previously_extracted2 = set()
        previously_extracted2.update([x.text for x in txtloc])

        while True:

            await page.evaluate("window.scrollTo(0, 0)")

            await asyncio.sleep(2)

            new_content = await page.content()
            soup = BeautifulSoup(new_content, "html.parser")

            new_msgloc = soup.find_all("div", attrs={"data-post": True})
            new_txtloc = soup.find_all(
                "div",
                class_={"etme_widget_message_text", "js-message_text"})

            new_post_ids = {x.get("data-post") for x in new_msgloc}
            new_elements = new_post_ids - previously_extracted

            if not new_elements:

                print("No new elements found. Ending extraction.")
                break

            for x, z in zip(set(new_msgloc), set(new_txtloc)):
                element_locator = x.get("data-post")
                # element_locator = x.get("data-post")
                txtloct = z.text
                print(f"New Post Locator: {element_locator}")
    
                msgins = Message(username=chname,
                                link=f"https://ble.ir/{chname}/{element_locator}",
                                text=txtloct,crawldate=ctime())
                await mongo_db.save_message(msgins)
                print(f"New Message Text: {txtloct}")
                
            previously_extracted.update(new_post_ids)
        chins=Channel(channel_name=name,bio=biog,username=f"@{chname}",counter_type= counter_types,counter_value=counter_values)
        await mongo_db.save_channel(chins)

    await page.close()
