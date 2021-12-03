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

    async def get_me(self) -> User:
        """获取机器人的信息"""
        result = await self._get(f"/users/@me")
        return User.parse_obj(result)

    async def get_guild_list(self) -> List[Guild]:
        """获取机器人加入的频道列表"""
        result = await self._get("/users/@me/guilds")
        return [Guild.parse_obj(_guild) for _guild in result]

    async def get_message(self, channel_id: str, message_id: str) -> Message:
        """获取指定子频道的消息"""
        result = await self._get(f"/channels/{channel_id}/messages/{message_id}")
        return Message.parse_obj(result)

    async def get_channel(self, channel_id: str) -> Channel:
        """获取子频道信息"""
        result = await self._get(f"/channels/{channel_id}")
        return Channel.parse_obj(result)

    async def get_guild_channel_list(self, guild_id: str) -> List[Channel]:
        """获取频道下的子频道列表"""
        result = await self._get(f"/guilds/{guild_id}/channels")
        return [Channel.parse_obj(_channel) for _channel in result]

    async def get_guild_info(self, guild_id: str):
        """获取频道信息"""
        result = await self._get(f"/guilds/{guild_id}")
        return Guild.parse_obj(result)

    async def get_member(self, guild_id: str, user_id: str) -> Member:
        """获取指定频道中成员的信息"""
        result = await self._get(f"/guilds/{guild_id}/members/{user_id}")
        return Member.parse_obj(result)

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