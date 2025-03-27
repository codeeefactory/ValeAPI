from asyncio import run
from time import sleep
from bs4 import BeautifulSoup

from playwright.async_api import async_playwright
# ec=enterchannel()
# gc=getchannel()
# joinedchlist=gc.chlist
# chlist=ec.chname_list
# # print(chlist)
async def leave( num, join_list):
            async  with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, timeout=50000)
                context = await browser.new_context(storage_state=f"auth_state_{num}.json")
                page = await context.new_page()
                for chname in join_list:
                    churl=f"https://web.bale.ai/@{chname}"
                    await page.goto(churl,wait_until="networkidle")
                    sleep(5)
                    # if chname not in joinedchlist:
                    lvbtn=page.locator('div.IconButton_innerWrapper__rOOEI.MoreMenu_IconButtonWrapper__pHUOP')
                    await lvbtn.wait_for(state="visible")
                    await lvbtn.click(force=True)
                    sleep(3)
                    
                    lv= page.locator("li.Menu_MenuItemWrapper__NyeOc")
                    await lv.wait_for(state="visible")
                    await lv.click(force=True)
                    
                    
                    # sleep(2)
                    lvconfirm= page.locator("button.ConfirmModal_ActionButton__5QiWH.ConfirmModal_isConfirm__CEJxO.css-128f583")
                    await lvconfirm.click(force=True)
                    
# num=input("num: ")
# leavelist= input("Enter the channel name you want to leave: ").split()
# run(join(num, leavelist))