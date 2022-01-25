import aiohttp
import json
from typing import Union

from .models import *
from .logger import Network

class GuildBotProtocol:
    async def _post(self, endpoint, data_map=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}{endpoint}", json=data_map, headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            }) as response:
                data = await response.text(encoding="utf-8")
                response.raise_for_status()
        Network.debug(f"POST {endpoint} 返回结果: {data}")
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return False

    async def _get(self, endpoint, params=None): 
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}{endpoint}", params=params, headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            }) as response:
                response.raise_for_status()
                data = await response.text(encoding="utf-8")
        Network.debug(f"GET {endpoint} 返回结果: {data}")
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return False
    
    async def _patch(self, endpoint, data_map=None):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{self.url}{endpoint}", json=data_map, headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            }) as response:
                data = await response.text(encoding="utf-8")
                response.raise_for_status()
        Network.debug(f"PATCH {endpoint} 返回结果: {data}")
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return False
    
    async def _delete(self, endpoint, data_map=None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.url}{endpoint}", json=data_map, headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            }) as response:
                Network.debug(f"DELETE {endpoint} 返回状态码: {response.status}")
                if response.status != 204:
                    return False
        return True
    
    async def _put(self, endpoint, data_map=None):
        async with aiohttp.ClientSession() as session:
            async with session.put(f"{self.url}{endpoint}", json=data_map, headers={
                'Authorization': self.token,
                'Content-Type': 'application/json'
            }) as response:
                Network.debug(f"PUT {endpoint} 返回状态码: {response.status}")
                if response.status != 204:
                    return False
        return True

    async def _get_gateway_url(self) -> str:
        """获取 Gateway URL"""
        result = await self._get("/gateway")
        return result["url"]
    
    async def _get_shards_gateway_url(self) -> Shards:
        """获取分片 Gateway URL"""
        result = await self._get("/gateway/bot")
        return Shards.parse_obj(result)

    '''
    用户 API
    '''
    async def get_me(self) -> User:
        """获取机器人的信息"""
        result = await self._get(f"/users/@me")
        return User.parse_obj(result)

    async def get_guild_list(self) -> List[Guild]:
        """获取机器人加入的频道列表"""
        result = await self._get("/users/@me/guilds")
        return [Guild.parse_obj(_guild) for _guild in result]

    '''
    频道 API
    '''
    async def get_guild_info(self, guild_id: str):
        """获取频道信息"""
        result = await self._get(f"/guilds/{guild_id}")
        return Guild.parse_obj(result)

    '''
    子频道 API
    '''
    async def get_guild_channel_list(self, guild_id: str) -> List[Channel]:
        """获取频道下的子频道列表"""
        result = await self._get(f"/guilds/{guild_id}/channels")
        return [Channel.parse_obj(_channel) for _channel in result]

    async def get_channel(self, channel_id: str) -> Channel:
        """获取子频道信息"""
        result = await self._get(f"/channels/{channel_id}")
        return Channel.parse_obj(result)

    async def create_channel(
        self,
        guild_id: str,
        name: str,
        sub_type: Union[int, ChannelSubType],
        position: int,
        parent_id: str,
        private_type: Union[int, PrivateType],
        private_user_ids: List[str],
        speak_permission: Union[int, SpeakPermission],
        application_id: Optional[str]
    ) -> Channel:
        """创建子频道"""
        result = await self._post(f"/guilds/{guild_id}/channels", {
            "name": name,
            "sub_type": sub_type,
            "position": position,
            "parent_id": parent_id,
            "private_type": private_type,
            "private_user_ids": private_user_ids,
            "speak_permission": speak_permission,
            "application_id": application_id
        })
        return Channel.parse_obj(result)

    async def edit_channel(
        self,
        channel_id: str,
        name: Optional[str],
        sub_type: Optional[Union[int, ChannelSubType]],
        position: Optional[int],
        parent_id: Optional[str],
        private_type: Optional[Union[int, PrivateType]],
        speak_permission: Optional[Union[int, SpeakPermission]],
    ) -> Channel:
        """修改子频道"""
        result = await self._patch(f"/channels/{channel_id}", {
            "name": name,
            "sub_type": sub_type,
            "position": position,
            "parent_id": parent_id,
            "private_type": private_type,
            "speak_permission": speak_permission
        })
        return Channel.parse_obj(result)

    async def edit_channel(self, channel_id: str) -> bool:
        """删除子频道"""
        return await self._delete(f"/channels/{channel_id}")

    '''
    成员 API
    '''
    async def get_member_list(self, guild_id: str, after: str, limit: int = 1) -> List[Member]:
        """获取频道成员列表"""
        result = await self._get(f"/guilds/{guild_id}/members", {
            "after": after,
            "limit": limit
        })
        return [Member.parse_obj(_member) for _member in result]

    async def get_member(self, guild_id: str, user_id: str) -> Member:
        """获取指定频道中成员的信息"""
        result = await self._get(f"/guilds/{guild_id}/members/{user_id}")
        return Member.parse_obj(result)

    async def delete_member(self, guild_id: str, user_id: str) -> bool:
        """删除频道成员"""
        return await self._delete(f"/guilds/{guild_id}/members/{user_id}")

    '''
    消息 API
    '''
    async def get_message(self, channel_id: str, message_id: str) -> Message:
        """获取指定子频道的消息"""
        result = await self._get(f"/channels/{channel_id}/messages/{message_id}")
        return Message.parse_obj(result)

    async def send_message(
        self,
        channel_id,
        content: Union[str, None] = None,
        embed: Union[MessageEmbed, None] = None,
        ark: Union[MessageArk, None] = None,
        image: Union[str, None] = None,
        message_id: Union[str, None] = None
    ) -> Message:
        """向子频道发送消息"""
        if content is None and embed is None and ark is None and image is None:
            ValueError("content, embed, ark, image 参数必选其一")
        data = {
            "msg_id": message_id
        }
        if content is not None:
            data["content"] = content
        if embed is not None:
            data["embed"] = embed.dict(exclude_none=True)
        if ark is not None:
            data["ark"] = ark.dict(exclude_none=True)
        if image is not None:
            data["image"] = image
        result = await self._post(f"/channels/{channel_id}/messages", data)
        return Message.parse_obj(result)

    '''
    频道身份组 API
    '''
    async def get_roles(self, guild_id: str) -> RoleRequest:
        """获取频道身份组列表信息，需要管理员权限"""
        result = await self._get(f"/guilds/{guild_id}/roles")
        return RoleRequest.parse_obj(result)

    async def create_roles(self, guild_id: str, filter: RolesFilter, info: RolesInfo) -> str:
        """创建一个频道身份组，需要管理员权限，返回 role_id"""
        result = await self._post(f"/guilds/{guild_id}/roles", {
            "filter": filter.dict(exclude_none=True),
            "info": info.dict(exclude_none=True)
        })
        return result["role_id"]

    async def edit_roles(self, guild_id: str, role_id: str, filter: RolesFilter, info: RolesInfo) -> dict:
        """修改频道身份组，需要管理员权限，返回 guild_id 与 role_id"""
        result = await self._patch(f"/guilds/{guild_id}/roles/{role_id}", {
            "filter": filter.dict(exclude_none=True),
            "info": info.dict(exclude_none=True)
        })
        return {
            "guild_id": result["guild_id"],
            "role_id": result["role_id"]
        }

    async def delete_roles(self, guild_id: str, role_id: str) -> bool:
        """删除频道身份组，需要管理员权限"""
        return await self._delete(f"/guilds/{guild_id}/roles/{role_id}")

    async def add_roles_members(self, guild_id: str, user_id: str, role_id: int, channel: Union[Channel, None] = None) -> bool:
        """增加频道身份组成员，需要管理员权限，`5-子频道管理员` 需要指定子频道"""
        data = None
        if role_id == DefaultRoles.channel_admin and channel is None:
            ValueError("`5-子频道管理员` 需要指定子频道")
        if role_id == DefaultRoles.channel_admin and channel is not None:
            data = {"channel": channel.dict(exclude_none=True)}
        return await self._put(f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}", data)


    async def delete_roles_members(self, guild_id: str, user_id: str, role_id: int, channel: Union[Channel, None] = None) -> bool:
        """删除频道身份组成员，需要管理员权限，`5-子频道管理员` 需要指定子频道"""
        data = None
        if role_id == DefaultRoles.channel_admin and channel is None:
            ValueError("`5-子频道管理员` 需要指定子频道")
        if role_id == DefaultRoles.channel_admin and channel is not None:
            data = {"channel": channel.dict(exclude_none=True)}
        return await self._delete(f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}", data)

    '''
    子频道权限 API
    '''
    async def get_member_permissions(self, channel_id: str, user_id: str) -> ChannelPermissions:
        """获取子频道用户权限"""
        result = await self._get(f"/channels/{channel_id}/members/{user_id}/permissions")
        return ChannelPermissions.parse_obj(result)

    async def edit_member_permissions(self, channel_id: str, user_id: str, add: str, remove: str) -> bool:
        """修改子频道用户权限"""
        return await self._put(f"/channels/{channel_id}/members/{user_id}/permissions", {
            "add": add,
            "remove": remove
        })

    async def get_role_permissions(self, channel_id: str, role_id: str) -> ChannelPermissions:
        """获取子频道身份组权限"""
        result = await self._get(f"/channels/{channel_id}/roles/{role_id}/permissions")
        return ChannelPermissions.parse_obj(result)

    async def edit_role_permissions(self, channel_id: str, role_id: str, add: str, remove: str) -> bool:
        """修改子频道身份组权限"""
        return await self._put(f"/channels/{channel_id}/roles/{role_id}/permissions", {
            "add": add,
            "remove": remove
        })

    '''
    私信 API
    '''
    async def create_direct_message(self, recipient_id: str, source_guild_id: str) -> DMS:
        """创建私信会话"""
        result = await self._post(f"/user/@me/dms", {
            "recipient_id": recipient_id,
            "source_guild_id": source_guild_id
        })
        return DMS.parse_obj(result)

    async def send_direct_message(
        self,
        guild_id,
        content: Union[str, None] = None,
        embed: Union[MessageEmbed, None] = None,
        ark: Union[MessageArk, None] = None,
        image: Union[str, None] = None,
        message_id: Union[str, None] = None
    ) -> Message:
        """发送私信"""
        if content is None and embed is None and ark is None and image is None:
            ValueError("content, embed, ark, image 参数必选其一")
        data = {
            "msg_id": message_id
        }
        if content is not None:
            data["content"] = content
        if embed is not None:
            data["embed"] = embed.dict(exclude_none=True)
        if ark is not None:
            data["ark"] = ark.dict(exclude_none=True)
        if image is not None:
            data["image"] = image
        result = await self._post(f"/dms/{guild_id}/messages", data)
        return Message.parse_obj(result)
    
    '''
    禁言 API
    '''
    async def mute_all(self, guild_id: str, mute_end_timestamp: Optional[int], mute_seconds: Optional[int]) -> bool:
        """禁言全员"""
        if mute_end_timestamp is not None:
            data = {"mute_end_timestamp": str(mute_end_timestamp)}
        elif mute_seconds is not None:
            data = {"mute_seconds": str(mute_seconds)}
        else:
            ValueError("mute_end_timestamp, mute_seconds 参数必选其一")
        if await self._patch(f"/guilds/{guild_id}/mute", data):
            return True
        return False

    async def unmute_all(self, guild_id: str) -> bool:
        return await self.mute_all(guild_id, mute_seconds=0)

    async def mute(self, guild_id: str, user_id: str, mute_end_timestamp: Optional[int], mute_seconds: Optional[int]) -> bool:
        """禁言指定成员"""
        if mute_end_timestamp is not None:
            data = {"mute_end_timestamp": str(mute_end_timestamp)}
        elif mute_seconds is not None:
            data = {"mute_seconds": str(mute_seconds)}
        else:
            ValueError("mute_end_timestamp, mute_seconds 参数必选其一")
        if await self._patch(f"/guilds/{guild_id}/members/{user_id}/mute", data):
            return True
        return False

    async def unmute(self, guild_id: str) -> bool:
        return await self.mute(guild_id, mute_seconds=0)
    
    '''
    公告 API
    '''
    async def create_guild_announces(self, guild_id: str, message_id: str, channel_id: str) -> Announces:
        """创建频道公告"""
        result = await self._post(f"/guilds/{guild_id}/announces", {
            "message_id": message_id,
            "channel_id": channel_id
        })
        return Announces.parse_obj(result)
    
    async def delete_guild_announces(self, guild_id: str, message_id: str) -> bool:
        """删除频道公告"""
        return await self._delete(f"/guilds/{guild_id}/announces/{message_id}")

    async def create_channel_id_announces(self, channel_id: str, message_id: str) -> Announces:
        """创建子频道公告"""
        result = await self._post(f"/channels/{channel_id}/announces", {
            "message_id": message_id
        })
        return Announces.parse_obj(result)
    
    async def delete_channel_id_announces(self, channel_id: str, message_id: str) -> bool:
        """删除子频道公告"""
        return await self._delete(f"/channels/{channel_id}/announces/{message_id}")
    
    '''
    日程 API
    '''
    async def get_schedule_list(self, guild_id: str, since: Optional[int]) -> List[Schedule]:
        """获取频道日程列表"""
        result = await self._get(f"/guilds/{guild_id}/schedules", {
            "since": since
        })
        return [Schedule.parse_obj(_schedule) for _schedule in result]

    async def get_schedule(self, channel_id: str, schedule_id: str) -> Schedule:
        """获取日程详情"""
        result = await self._get(f"/channels/{channel_id}/schedules/{schedule_id}")
        return Schedule.parse_obj(result)

    async def create_schedule(self, channel_id: str, schedule: Schedule) -> Schedule:
        """创建日程"""
        result = await self._post(f"/channels/{channel_id}/schedules", {
            "schedule": schedule
        })
        return Schedule.parse_obj(result)

    async def edit_schedule(self, channel_id: str, schedule_id: str, schedule: Schedule) -> Schedule:
        """修改日程"""
        result = await self._patch(f"/channels/{channel_id}/schedules/{schedule_id}", {
            "schedule": schedule
        })
        return Schedule.parse_obj(result)

    async def delete_schedule(self, channel_id: str, schedule_id: str) -> bool:
        """删除日程"""
        return await self._delete(f"/channels/{channel_id}/schedules/{schedule_id}")