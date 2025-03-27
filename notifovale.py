from time import ctime, sleep
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
        while True:
            try:
                sleep(5)
                await page.reload(wait_until="networkidle")
                
        await page.wait_for_load_state("networkidle")
        last_seen_message = None