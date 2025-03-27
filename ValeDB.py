from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List

from sympy import li

class Channel(BaseModel):
    channel_name: Optional[str] = None
    bio: Optional[str] = None
    username: Optional[str] = None
    counter_type: Optional[str] = None
    counter_value: Optional[str] = None
    is_joined: Optional[bool] = None

class ChannelInfo(BaseModel):
    channel_name: Optional[str] = None
    bio: Optional[str] = None

class Group(BaseModel):
    name: Optional[str] = None
    group_bio: Optional[str] = None
    
    user_list: Optional[List[str]] = None# List of users can be None
    user_bio: Optional[list] = None
    user_last_seen: Optional[list] = None
    user_usermame: Optional[str] = None
        
class Message(BaseModel):
    username: Optional[str] = None
    link: Optional[str] = None
    text: Optional[str] = None
    senddate: Optional[str] = None
    crawldate: Optional[str] = None
    
# class GroupUser(BaseModel):
#     user_id: Optional[str] = None
#     user_name: Optional[str] = None
#     user_bio: Optional[str] = None
#     user_last_seen: Optional[str] = None
class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.channel_collection = self.db["channels"] 
        self.users_collection = self.db["users"]
        self.group_collection = self.db["groups"]
        self.message_collection = self.db["Messages"]

    # Save channel
    async def save_channel(self, channel: Channel):
        await self.channel_collection.insert_one(channel.model_dump(exclude_none=True))  # exclude_none=True ensures null values are excluded

    # Save message
    async def save_message(self, message: Message):
        await self.message_collection.insert_one(message.model_dump(exclude_none=True))  # exclude_none=True ensures null values are excluded

    # Save group
    async def save_group(self, group: Group):
        await self.group_collection.insert_one(group.model_dump(exclude_none=True))  # exclude_none=True ensures null values are excluded

    # Save users
    # async def save_users(self, groupinf: GroupInfo):
    #     group_doc = await self.users_collection.find_one()  # Assuming only one group for simplicity
    #     if group_doc:
    #         group = Group(**group_doc)  # Populate the Group object from the database
    #         group.name = group.name  # Assign the actual name later
    #         self.users_collection = self.db[group.name]  # Use the newly assigned name as collection name

    #     await self.users_collection.insert_one(groupinf.model_dump(exclude_none=True))  # exclude_none=True ensures null values are excluded

    # Get all channels
    async def get_all_channels(self):
        channels = await self.channel_collection.find().to_list(100)
        return channels

    # Get all groups
    async def get_all_groups(self):
        groups = await self.group_collection.find().to_list(100)
        return groups

    async def close(self):
        await self.client.close()
