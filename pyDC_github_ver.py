#導入Discord.py
import discord
import time
import asyncio
import os
import keep_alive

#初始化token
my_secret = os.environ['robot_token']

#初始化存訊息的list
tmp=[' ']*10000

#有多少條提醒了
global times
times=int(0)

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用event函式庫
@client.event

#當機器人完成啟動時在console顯示
async def on_ready():
    print('目前登入身份：',client.user)
    asyncio.create_task(main())

#調用event函式庫
@client.event

#當有訊息時
async def on_message(message):
    global times
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果以「不嘎嘎嘎請提醒我」開頭
    if message.content.startswith('不嘎嘎嘎請提醒我'):
      #分割訊息成三份
      temp = message.content.split(" ",3)
      #如果分割後串列長度只有1或2
      if len(temp) == 1 or len(temp)==2:
        await message.channel.send("你要我提醒什麼講清楚")
      else:
        await message.add_reaction('👍')
        #await message.channel.send(f"<@%s>成功！"%message.author.id)
        for i in range (3):
            tmp[i+5*times]=temp[i]
        tmp[3+5*times]=message.author.id
        tmp[4+5*times]=message.channel.id
        times+=1
#發訊息的main
async def main():
    global times
    while True:
        #print("運行中...times=",times)
        if int(time.strftime("%S",time.localtime()))==0:
            for i in range(times+1):
                if(tmp[i*5+1]==time.strftime("%H:%M",time.localtime())):
                    #底下記得改頻道ID
                  await client.get_channel(int(tmp[i*5+4])).send("<@%s>"%tmp[i*5+3]+tmp[i*5+2])
                  tmp[i*5+2]=""
                    #await asyncio.sleep(60-int(time.strftime("%S",time.localtime())))
        await asyncio.sleep(1)

#身分/持續運行
keep_alive.keep_alive()
client.run('%s'%my_secret) #TOKEN
