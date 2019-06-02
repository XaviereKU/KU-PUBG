import asyncio
import discord
import requests
from bs4 import BeautifulSoup
import lxml
import json
from collections import OrderedDict
import random
import math
import stats
import os

client = discord.Client()

token = os.environ["token"]
API_KEY = os.environ["API_KEY"]

#API header
header = {
    "Authorization": API_KEY,
    "Accept": "application/vnd.api+json"
}

statusurl = 'https://api.pubg.com/status'
status = str(requests.get(statusurl))
if status == '<Response [200]>':
	season = stats.getseason(header)

@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print("===========")
    await client.change_presence(game=discord.Game(name="고파스 배그도우미", type=1))

@client.event
async def on_member_join(member):
    server = member.server
    channel = discord.Object('437610447810854923')
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(channel, fmt.format(member, server))


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    id = message.author.id
    channel = message.channel

    if message.content == '/구직' or message.content == '/구인' or message.content == '/ㄱㅇ' or message.content == '/ㄱㅈ' or message.content == '/RW' or message.content == '/rw' or message.content == '/RD' or message.content == '/rd':
        member = message.author
        voice = message.author.voice.voice_channel

        if voice == None:
            fmt = '@here {0.display_name} 구직합니다!'
            await client.send_message(channel, fmt.format(member))
        else:
            member = voice.voice_members
            if voice.name.startswith('듀오'):
                cnt = max(2 - len(member), 0)
            else:                
                cnt = max(4 - len(member), 0)
            if cnt > 0:
                fmt = '@here {0.name} 에서 ' + cnt.__str__() + ' 명 구인합니다!'
            else:
                fmt = '{0.name} 풀방입니다!'
            await client.send_message(channel, fmt.format(voice))

    if message.content == '/고파스' or message.content == '/koreapas':
        await client.send_message(channel, 'https://www.koreapas.com/bbs/main.php')

    if message.content == '/초대':
        invite = await client.create_invite(message.channel, xkcd = True, max_age=0, max_uses=1)
        await client.send_message(message.author,"Your invite URL is {}".format(invite.url))

    if message.content == '/롤' or message.content == '/lol' or message.content == '/칼바람' :
        await client.send_message(channel, "롤 주소는 https://discord.gg/y6qVgBs")

    if message.content == '/망겜' or message.content == '/공카':
        await client.send_message(channel, 'PUBG 공식 카페 공지사항 : <https://goo.gl/n45ZBj>')      
        
    if message.content == '/거울':
        rnd = random.randrange(1, 100)
        if 0 < rnd <= 70:
            await client.send_message(channel, '응 머머리오징어 안녕?')
        if 70 < rnd <= 99:
            await client.send_message(channel, '응 너 얼굴 아사리판')
        elif 99 < rnd :
            await client.send_message(channel, '그 얼굴로 왜 게임하세요ㅠㅠ')
        
    if message.content == '/test':
        global status
        if message.author.id == '328859649069809664':
            await client.send_message(channel, '```평일 : 18:30~익일 09:00 근무\n 주말은 종일 근무```')
            print(status)
        else:
            return None

    if message.content.startswith('/전적') or message.content.startswith('/stat') or message.content.startswith('/핵'):
        global season
        global status
        if status == '<Response [200]>':
	        text = message.content
	        result = stats.getstat(text,header,season)
	        if type(result) == str:
	            await client.send_message(channel,result)
	        else:
	            await client.send_message(channel, embed=result)
        else:
        	await client.send_message(channel, '서버 오류. 잠시 후 다시 시도해 주세요.')

    if message.content == '/?' or message.content =='/help' or message.content =='/봇':
        embed = discord.Embed(color=0x4e7ecf)
        embed.add_field(name='/? /help /봇', value='도움말', inline=False)
        embed.add_field(name='/롤 /lol', value='칼바람내전', inline=False)
        embed.add_field(name='/고파스 /koreapas', value='고파스!', inline=False)
        embed.add_field(name='/구인 /구직 /ㄱㅈ /ㄱㅇ', value='구인구직(보이스 참여여부에 따라 자동인식)', inline=False)
        embed.add_field(name='/초대 ', value='1회용 초대 주소 생성', inline=False)
        embed.add_field(name='/전적, /핵, /stat', value='전적검색. /전적?로 사용법을 알 수 있습니다.\n 라운드 종료 후 갱신됩니다.', inline=False)
        embed.set_footer(text = 'KU_PUBG Bot ver.181007')
        await client.send_message(channel, embed=embed)
        
client.run(token)

#2018.02.11 최초 작성자 - SBS84
#2018.02.15 최종 수정 - XaviereKU
#2018.02.16 핵 의심 검색 추가 - XaviereKU
#2018.02.19 embed가 None이 아닐때만 출력됨 - XaviereKU
#2018.02.23 각종 오류 해결, /서버 명령어 추가
#2018.02.26 노가리방에서 구직시 구직 메시지 띄움. 구인 명령어시 노가리깔 사람 구하는 메시지 띄움.
#2018.02.28 주사위 기능 추가, 전적 검색 오류 수정, 서버 상태에 접속 불가 추
#2018.03.08 전적 검색 알리미 두 번 나오는 것 해결
#2018.03.15 카카오 핵 검색 추가
#2018.03.17 핵 전적 검색시 nickname 존재여부 확인
#2018.03.26 망겜 명령어 추가
#2018.04.24 오타 수정
#2018.04.25 핵에 평댐과 게임수 추가
#2018.05.10 공식 API로 변경
#2018.05.18 로또기능 제거, embed footer 추가.
#2018.08.20 서버 명령어 삭제
#2018.08.20 시즌 자동화
#2018.09.18 핵 명령어 수정
#2018.09.20 전적에 판수 추가.
#2018.10.04 API 업데이트 반영 및 핵 명령어 전적과 통합.
#2019.06.02 API 서버 상태 체크 후 작동
