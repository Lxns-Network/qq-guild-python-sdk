import asyncio
import aiohttp
import inspect
import json

from typing import Callable

from .models.ws import Intents, Load, opcode
from .protocol import GuildBotProtocol
from .logger import Network, Protocol, Session, Event

class GuildBot(GuildBotProtocol):
    def __init__(self, app_id, token, sandbox=True, intents: Intents = Intents()):
        self.url = 'https://api.sgroup.qq.com'
        if sandbox:
            self.url = 'https://sandbox.api.sgroup.qq.com'
            Protocol.info("当前为沙箱环境")

        self.token = f"Bot {app_id}.{token}"
        self.intents = intents.to_int()
        self.ws = None

        self.s = 0
        self.heartbeat_interval = 0
        self.session = None

        self._handlers = {}

    def run(self, loop=None):
        loop = loop or asyncio.new_event_loop()
        loop.run_until_complete(self._run_async())

    async def _run_async(self):
        session = aiohttp.ClientSession()
        gateway_url = await self._get_gateway_url()
        self.ws = await session.ws_connect(gateway_url)
        await self.ws_event()
    
    async def _auth(self):
        if self.session == None:
            load = {
                "op": opcode.Identify,
                "d": {
                    "token": self.token,
                    "intents": self.intents,
                    "shard": [0, 1],
                    "properties": {
                        "$os": "linux",
                        "$browser": "python_sdk",
                        "$device": "server"
                    }
                }
            }
        else:
            load = {
                "op": opcode.Resume,
                "d": {
                    "token": self.token,
                    "session_id": self.session,
                    "seq": 1337
                }
            }
        await self.ws.send_json(load)
    
    async def _heartbeat(self):
        while self._heartbeat:
            await asyncio.sleep(self.heartbeat_interval)
            try:
                Network.info("发送心跳")
                await self.ws.send_json({
                    "op": opcode.Heartbeat,
                    "d": self.s
                })
            except:
                continue

    async def ws_event(self):
        while True:
            message = await self.ws.receive()
            Network.debug(f"接收内容: {message.data}")
            if isinstance(message.data, int):
                if message.data == 4009:
                    Network.warn("连接过期，尝试重新登录")
                elif message.data >= 4900:
                    Network.warn("内部错误，尝试重新登录")
                else:
                    Network.error(f"发生意料之外的 opcode: {message.data}")
                    return
                # self.session = None
                await self._run_async()
                return
            try:
                message = json.loads(message.data)
            except:
                if message.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    Network.info("连接已断开，尝试重连")
                    await self._auth()
                continue
            load = Load(**message)
            op = load.op
            if op == opcode.Hello:
                self.heartbeat_interval = load.d.heartbeat_interval / 1000
                await self._auth()
            elif op == opcode.Dispatch:
                self.s = load.s
                t = load.t
                if t == "READY":
                    self.session = load.d.session_id
                    Session.info(f"已连接: @{load.d.user.username} ({load.d.user.id})")
                    asyncio.create_task(self._heartbeat())
                elif t == "RESUMED":
                    Network.info("重连成功")
                self.event_handler(t, load.d) # 发送给事件处理器
            elif op == opcode.InvalidSession:
                Network.warn("连接参数错误，尝试重新登录")
                self.session = None
                await self._auth()
            elif op == opcode.Reconnect:
                Network.info("服务端通知重连，开始重连")
                await self._auth()
            elif op == opcode.HeartbeatACK:
                Network.info("收到心跳响应")
    
    def add_event_handler(self, event_name, handler):
        self._handlers.setdefault(event_name, [])
        self._handlers[event_name].append(handler)
        
    def event_handler(self, event_name, event_data):
        if self._handlers.get(event_name) is None:
            return
        for handler in self._handlers[event_name]:
            Event.info(f"处理事件: {event_name}")
            asyncio.create_task(handler(self, event_data))

    def receiver(self, event_name):
        def receiver_warpper(handler: Callable):
            if not inspect.iscoroutinefunction(handler):
                raise TypeError("event body must be a coroutine function.")
            
            self.add_event_handler(event_name, handler)
            return handler

        return receiver_warpper