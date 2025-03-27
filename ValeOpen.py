import asyncio
from time import sleep
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from ValeDB import Message, MongoDB, Channel

async def get_channel(num):
    mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="eitaa")
    async with async_playwright() as p:
       
        
        browser = await p.chromium.launch(headless=False, timeout=50000)
        context = await browser.new_context(storage_state=f"auth_state_{num}.json")
        page = await context.new_page()

        await page.goto("https://web.bale.ai/chat")
        await page.wait_for_selector('span.text-super', timeout=50000)
        await page.wait_for_timeout(3000)
        
        spans = page.locator('span.text-super', has_text="کانال").first
        await spans.click(force=True)
        await page.wait_for_timeout(5000)
     
        ch = page.locator("div.DialogTabContent_TabContainer__6cy4L")
        chloc = ch.locator("div[data-test-id='virtuoso-scroller']")
        chloc2 = chloc.locator("div[data-test-id='virtuoso-item-list']")
        indexx=0
        
        while True:
            # Try to find the div with the current data-item-index
            chel = chloc2.locator(f'div[data-item-index="{indexx}"]').last

            # If the element exists (is visible and available), click on it
           
            print(f'Clicking on div with data-item-index="{indexx}"')
            await chel.click(force=True)
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
            a=[]
            b=[]
            for i in await chloc.element_handles():
                await i.wait_for_element_state("visible")
                await i.click(force=True)
                channel_name = await i.text_content()
                
                a.append(page.url)
                await page.wait_for_timeout(6000)
                for x in a:
                    b.append(str(x).replace("https://web.bale.ai/#@",""))
                    
                # print(b)
            for j in set(b):
                    
                    print(j)
                    page2=await context.new_page()
                    await page2.goto(f"https://ble.ir/@{j}")
                    # sleep(2)
                    soup= BeautifulSoup(await page2.content(),features="html.parser")
                
                
                
                   
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
                            txtloct = z.text
                            print(f"New Post Locator: {element_locator}")
                            msgins = Message(username=j,
                                            link=f"https://eitaa.com/{element_locator}",
                                            text=txtloct)
                            await mongo_db.save_message(msgins)
                            print(f"New Message Text: {txtloct}")

                        previously_extracted.update(new_post_ids)
                    
                    
                # await page.locator('div.content').click(force=True)
                
                # #usernamee=page.locator('div.row-title.tgico.tgico-username').text_content()
                
                # #row-title tgico tgico-info pre-wrap
                # biog=page.locator('row-title.tgico.tgico-info.pre-wrap')
                # bogtex=await biog.text_content()
                    print(biogr)
                    print(name)
                    print(channel_name)
                    intodb=Channel(channel_name=str(name),bio=str(biogr),username=str(page2.url),is_joined=True)
                    await mongo_db.save_channel(intodb)
                    # sleep(2)
                # print(a)
                
                
            await browser.close()
