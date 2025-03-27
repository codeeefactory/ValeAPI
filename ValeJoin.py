from asyncio import run
from time import sleep
from playwright.async_api import async_playwright
from ValeDB import MongoDB, Channel

async def join_and_save_channels(num, join_list):
    mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="ValeDB")  
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, timeout=50000)
        context = await browser.new_context(storage_state=f"auth_state_{num}.json")
        page = await context.new_page()
        
        for chname in join_list:
            churl = f"https://web.bale.ai/@{chname}"
            await page.goto(churl,wait_until="networkidle")
            # sleep(15)
            # Click the join button
            
            await page.locator("button.NewButton_Button__nfU0M.NewButton_Full__twHH5.NewButton_Filled__-Io2I.Join_joinButton__gJLfd").click(force=True)
            sleep(10)
            
            # Save channel info to MongoDB after joining
            channel_data = Channel(channel_name=chname, user_id=num)
            await mongo_db.save_channel(channel_data)
            print(f"Joined and saved channel: {chname}")
        
        await browser.close()

# if __name__ == "__main__":
#     num = input("num: ")
#     joinlist = input("Enter the channel name(s) you want to join: ").split()

#     # MongoDB client
#     mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="eitaa", collection_name="joined_channels")

#     run(join_and_save_channels(num, joinlist, mongo_db))
