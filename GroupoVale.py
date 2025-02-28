import asyncio
from os import name
from time import sleep
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from ValeDB import MongoDB, Group
import os
import hashlib
from requests import get
from asyncio import run
def find_duplicates(directory):
    file_hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            hash_value = hash_file(file_path)

            if hash_value in file_hashes:
                duplicates.append((file_path, file_hashes[hash_value]))
            else:
                file_hashes[hash_value] = file_path
    return duplicates

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()
async def get_group(num):
        mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="eitaa")
        usersbio=[]
        users_usernames=[]
        p=await async_playwright().start()
        browser = await p.chromium.launch(headless=False, timeout=50000)
        context = await browser.new_context(storage_state=f"auth_state_{num}.json")
        page = await context.new_page()

        await page.goto("https://web.bale.ai/chat", wait_until="networkidle")
        sleep(3)
        gps = page.get_by_text("گروه").first
        await gps.click(force=True)
        sleep(2)

        gp = page.locator("div.DialogTabContent_TabContainer__6cy4L")
        gploc = gp.locator("div[data-test-id='virtuoso-scroller']")
        gploc2 = gploc.locator("div[data-test-id='virtuoso-item-list']")
        indexx=0
        
        while True:
            # Try to find the div with the current data-item-index
            gpel = gploc2.locator(f'div[data-item-index="{indexx}"]').last

            # If the element exists (is visible and available), click on it
           
            print(f'Clicking on div with data-item-index="{indexx}"')
            await gpel.click(force=True)
            group_name=await page.locator("div[class='ChatAppBar_Name__OxftE']").text_content()
           
            await page.wait_for_timeout(1500)
            # else:
            #     print(f'No more divs found with data-item-index="{indexx}", stopping.')
            #     break
            indexx += 1

            info=page.locator("div[class='main-section-container ChatWrapper_BodyWrapper__qZMt+ css-gtzxlz']")
            await info.locator("div[class='ChatAppBar_AppbarWrapper__zWr9N']").click(force=True)
        

            print(group_name)
            os.makedirs(group_name,exist_ok=True)
            sleep(1)
            peer_titles = await page.eval_on_selector_all(
                ".css-1tawzay",
                "elements => elements.map(element => element.textContent.trim())",
            )
            peer_ids = await page.eval_on_selector_all(
            '.e2893hg5',
            'elements => elements.map(el =>el.textContent.trim())'
        )

            for peer_id in peer_ids:
                await page.click(peer_id)
                biouser=  page.locator('.Text_text__0QjN9 , span')
                username= await page.query_selector('.Text_text__0QjN9 , span')
                imgloc= page.locator("div.profile-avatars-container")
                avloc= page.locator("div.profile-avatars-avatars")
                
                nextimg=page.locator("span.tgico-down.media-viewer-next-button")
                
             
                # print(await biouser.inner_text())
                print(await username.inner_text())
        #         count = await imgloc.count()
        #         if count > 0:
        #             await page.click("div.profile-avatars-arrow.profile-avatars-arrow-next.tgico-avatarnext")
        #             # await page.click("div.profile-avatars-arrow.profile-avatars-arrow-next.tgico-avatarnext")
                    
        #             sleep(3)
        #             await imgloc.click(force=True)
        #             download_path=f"{group_name}/"
        #             while True:
        #                 async with page.expect_download() as download_info:
        #                     # await v.wait_for_element_state(state="stable")
        #                     # await v.click()
        #                     await page.wait_for_selector("button.btn-icon.tgico-download")
        # # Perform the action that initiates download
        # # await page.get_by_text("Download file").click()
                            
        #                     downloc=page.locator("button.btn-icon.tgico-download")
        #                     await downloc.click(force=True)
        #                     download = await download_info.value  # This will give you the download object
        #                     print(f"Download started: {download.suggested_filename}")
                            
        #                     await download.save_as(download_path + download.suggested_filename);import pdb; pdb.set_trace()
        #                     if  await nextimg.is_visible():
        #                         await nextimg.click(force=True)
        #                     # if find_duplicates():
        #                     #     break
        #                     #  sleep(1)
        #                     mediaviewerloc=page.locator("div.media-viewer-topbar.media-viewer-appear")
        #                     await mediaviewerloc.wait_for(state='visible')
        #                     # await page.goto(churl,wait_until="networkidle")
        #                     closeloc=mediaviewerloc.locator("button.btn-icon.tgico-close").last
        #                     sleep(0.5)
                            
        #                     await closeloc.wait_for(state='visible')        
        #                     await closeloc.click(force=True)
                                
        #             # imgsrc=[]
        #             # src=await page.query_selector("img.thumbnail")
        #             # imgsrc.append(src.get_attribute('src'))
        #             # await nextimg.click(force=True)
        #             # src=await page.query_selector("img.thumbnail")
        #             # imgsrc.append(src.get_attribute('src'))
        #             # ii=0
        #             # while imgsrc[ii]!=imgsrc[ii+1]:
        #             #     await nextimg.click(force=True)
        #             #     src=await page.query_selector("img.thumbnail")
        #             #     imgsrc.append(src.get_attribute('src'))
        #             #     ii+=1
        #         # await page.click("div.sidebar-content div.scrollable.scrollable-y.no-parallax div.profile-content div.profile-avatars-container div.profile-avatars-avatars")
        #     #             parent_div_selector = await img.evaluate('el => el.closest("div.profile-avatars-avatar.media-container")?.getAttribute("id")')
        #     # if parent_div_selector:
        #     #     parent_div = await page.query_selector(f"div# {parent_div_selector}")
        #     #     if parent_div:
        #     #         await parent_div.click()
        #     #         print("Clicked on the div!")
        #         sleep(2)
            
        #         await page.click('div.chat.tabs-tab.type-chat.active div.sidebar-header.topbar button.btn-icon.tgico-left.sidebar-close-button')
        #     # for peer in peer_titles:
        #     #     userloc=page.get_by_text(peer).first
        #     #     await userloc.click(force=True)
        #     #     await page.go_back()
                
        #     last_seen = await page.eval_on_selector_all(
        #         ".search-super-content-members .dialog-subtitle .user-last-message .i18n",
        #         "elements => elements.map(element => element.textContent.trim())",
        #     )
        #     biogp=  page.locator('div.row-title.tgico.tgico-info.pre-wrap')
        #     # peer_images = await page.eval_on_selector_all(
        #     #     ".search-super-content-members .avatar-photo",
        #     #     "elements => elements.map(element => element.src)",
        #     # )

        #     comb = {}
        #     comb = dict(zip(peer_titles, last_seen))
        #     print(comb)
        #     print(await biogp.inner_text())
        #     # async with aiohttp.ClientSession() as session:
        #     #     tasks = []
        #     #     for image_url, filename in zip(peer_images, peer_titles):
        #     #         task = download_image(session, image_url, filename)
        #     #         tasks.append(task)

        #     #     # Wait for all downloads to finish
        #     # await asyncio.gather(*tasks)
        #     groupins = Group(
        #         name=str(group_name),
        #         user_list=peer_titles,
        #         user_last_seen=last_seen,
        #         group_bio=await biogp.inner_text(),
        #         user_usermame=await username.inner_text()
        #     )
        #     await mongo_db.save_group(groupins)

        # await browser.close()
run(get_group("9129252158"))