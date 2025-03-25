from ast import Dict, List
from asyncio import run
from pdb import set_trace
from re import L
from fastapi import FastAPI, HTTPException, BackgroundTasks

from fastapi.responses import JSONResponse
from pydantic import BaseModel
# from countmsg import countmsgs
# from getchat import get_channel
# from getgp import get_group
from ValeDB import MongoDB
from Savemsg import getmsgs
# import getmedia
# import getvideo
# import getphoto
# from ValeJoin import join_and_save_channels
# from ValeDB import leave
from auth import save
from playwright.async_api import async_playwright
from asyncio import sleep as async_sleep

import videoapi

app = FastAPI()


mongo_db = MongoDB(uri="mongodb://localhost:27017", db_name="ValeDB")


class base(BaseModel):
    num: str


class ChannelRequest(BaseModel):
    join_list: list


class ScrapingRequest(BaseModel):
    num: str
    chlist: list


@app.on_event("startup")
async def startup_db():
    print("FastAPI is starting.")


@app.on_event("shutdown")
async def shutdown_db():
    await mongo_db.close()
    print("FastAPI has shut down.")


class AuthRequest(BaseModel):
    num: str
    count:str

class OTPRequest(BaseModel):
    session_id: str
    otp: str
class withoutnum(BaseModel):
    chlist:list

@app.post("/auth/")
async def start_auth(background_tasks: BackgroundTasks, request: AuthRequest):
    try:
        
        background_tasks.add_task(save,request.count,request.num)
        return {"message": "OTP sent to your phone number"}
    
        # await auth_instance.save(request.num)
        return {"message": "OTP sent to your phone number"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/get_channel/")
# async def scraping_channel(request: base, background_tasks: BackgroundTasks):
#     try:
#         background_tasks.add_task(get_channel, request.num)

#         return {
#             "message": f"Channel scraping from account {request.num} started ,return to console to see channel names"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/start_group/")
# async def scraping_group(request: base, background_tasks: BackgroundTasks):
#     try:
#         background_tasks.add_task(get_group, request.num)

#         return {"message": "Scraping process started!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/channels/")
# async def get_channels():
#     try:
#         channels = await mongo_db.get_all_channels()
#         return {"channels": channels}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/join_channel/")
# async def joining_channel(request: ScrapingRequest, background_tasks: BackgroundTasks):
#     try:
#         background_tasks.add_task(join_and_save_channels, request.num, request.chlist)

#         return {"message": f"join to {request.chlist} started!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/leave_channel/")
# async def leaving_channel(request: ScrapingRequest, background_tasks: BackgroundTasks):
#     try:
#         background_tasks.add_task(leave, request.num, request.chlist)

#         return {"message": f"leave {request.chlist} started!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/groups/")
# async def get_groups(background_tasks: BackgroundTasks, request: base):
#     try:
#         background_tasks.add_task(get_group, request.num)

#         return {"groups started"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_messages/")
async def get_messages(background_tasks: BackgroundTasks, request: withoutnum):
    try:
        background_tasks.add_task(getmsgs, request.chlist)
        return {f"get message from {request.chlist} start"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @app.post("/count_messages/")
# async def count_messages(background_tasks: BackgroundTasks, request: ScrapingRequest):
#     try:
#         background_tasks.add_task(countmsgs, request.num, request.chlist)
#         return {f"get new message from {request.chlist} has  started"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
@app.post("/get_video/")
async def get_vedio(background_tasks: BackgroundTasks, request: ScrapingRequest):
    try:
        background_tasks.add_task(videoapi.getvideo, request.num, request.chlist)
        return {f"get media from {request.chlist} start"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @app.post("/get_photo/")
# async def get_photo(background_tasks: BackgroundTasks, request: ScrapingRequest):
#     try:
#         background_tasks.add_task(getphoto.getphoto, request.num, request.chlist)
#         return {f"get photos from {request.chlist} start"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @app.post("/get_media/")
# async def get_media(background_tasks: BackgroundTasks, request: ScrapingRequest):
#     try:
#         background_tasks.add_task(getmedia.get_media, request.num, request.chlist)
#         return {f"get all media from {request.chlist} start"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))