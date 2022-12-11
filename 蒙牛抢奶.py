import asyncio
from aiohttp import ClientSession
import time
import json
import hashlib
import random
import string
import requests
import base64
import execjs
from datetime import datetime
import sys
#解包可得
clientKey="FIDBFh4U65amvCDIlvE92WECR8txa48K"
clientSecret="qzEKyCTxQdaquxm5u2OJKB3bVTie4f9qHTQIDTIGxCc88egeIAyJ6QXQeow8whvU"
抢购链接="https://mengniu-apig.xiaoyisz.com/mengniu-world-cup-1122/mp/api/user/seckill/ghg3/dff/dd2/dsfs2/e21d/vddc"
jsonId=1000021



Authorization=""




Phone_UA='Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.30(0x18001e32) NetType/WIFI Language/zh_CN'
work_count=10#线程数
run_count=200
buy_times='2022-12-12 08:59:57.500'
step_error_time_ms=500#误差时间


class Timer(object):
    def __init__(self, sleep_interval=0.5):

        self.buy_time = datetime.strptime(buy_times,"%Y-%m-%d %H:%M:%S.%f")
        # self.buy_time = buy_time_config
        print("购买时间：{}".format(self.buy_time))

        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000)
        self.sleep_interval = sleep_interval

        self.diff_time = self.local_mn_time_diff()

    def mn_time(self):
       
        url = 'https://mengniu-apig.xiaoyisz.com/mengniu-world-cup-1122/mp/public/api/timestamp'
        header={
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.30(0x18001e32) NetType/WIFI Language/zh_CN',
            'Authorization':Authorization,
            'Referer':url
        }
        ret = requests.get(url,headers=header).text
        js = json.loads(ret)
        if(js["code"]==0):
            timeStamp = float(js["data"]/1000) 
            timeArray = time.localtime(timeStamp) 
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 
            print('服务器时间',otherStyleTime)
            return int(js["data"])
        

    def local_time(self):
        """
        获取本地毫秒时间
        :return:
        """
        return int(round(time.time() * 1000)) - int(step_error_time_ms)

    def local_mn_time_diff(self):
        """
        计算本地与服务器时间差
        :return:
        """
        return self.local_time() - self.mn_time()

    def start(self):
        # print(datetime.now())
        
        print('正在等待到达设定时间:{}，检测本地时间与服务器时间误差为【{}】毫秒'.format(self.buy_time, self.diff_time))
        while True:
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                print('时间到达，开始执行……',int(round(time.time() * 1000)))
                break
            else:
                time.sleep(self.sleep_interval)




def DES解密(data):
    return context.call('DES_Decrypt',data)


    
def 随机字符串(length):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, length))
    return ran_str

def 获取参数签名(nonce,timestamp):
    data="clientKey="+clientKey+"&clientSecret="+clientSecret+"&nonce="+nonce+"&timestamp="+str(timestamp)
    md5hash = hashlib.md5(data.encode('utf-8')).hexdigest().upper()
    return md5hash
def 获取请求头签名(rk,requestId,timestamp):
    key=DES解密(rk)
    data="requestId="+requestId+"&timestamp="+str(timestamp)+"&key="+key
    return hashlib.md5(data.encode('utf-8')).hexdigest()
async def 获取RK():
    try:
        url="https://mengniu-apig.xiaoyisz.com/mengniu-world-cup/mp/api/user/baseInfo"
        
        nonce=随机字符串(16)
        
        timestamp=int(round(time.time() * 1000))
        param={
            "timestamp":timestamp,
            "nonce":nonce,
            "signature":获取参数签名(nonce,timestamp)
        }
        
        header={
            'User-Agent':Phone_UA,
            'Authorization':Authorization,
            'Referer':url
        }
        
        ##print(requests.get(url=url, params=param, headers=header).text)
        async with session.get(url=url,params=param,headers=header) as response:
                res = await response.json()
                
                if(res['code']==0):
                    rk=res['data']['rk']
                    print("rk:",rk)
                    return rk 
                else:
                    print(res)
            
                
                
    except Exception as e:
        print("运行出错",e)

async def 查询中奖():
    try:
        url="https://mengniu-apig.xiaoyisz.com/mengniu-world-cup/mp/api/user/goods/list"
        nonce=随机字符串(16)
        timestamp=int(round(time.time() * 1000))
        param={
            "page":1,
            "pageSize":100,
            "timestamp":timestamp,
            "nonce":nonce,
            "signature":获取参数签名(nonce,timestamp)
        }
        header={
            'User-Agent':Phone_UA,
            'Authorization':Authorization,
            'Referer':url
        }
        
        ##print(requests.get(url=url, params=param, headers=header).text)
        async with session.get(url=url,params=param,headers=header) as response:
                res = await response.json()
                if(res['code']==0):
                    for line in res['data']:
                        print(line['sources'],line['createTime'])
            
    except Exception as e:
        print("运行出错",e)

async def 开抢():
    try:
        url=抢购链接
        timestamp=int(round(time.time() * 1000))
        requestId=随机字符串(32)
        header={
            'User-Agent':Phone_UA,
            'Authorization':Authorization,
            'Referer':url,
            'RequestId':requestId,
            'Timestamp':str(timestamp),
            'Sign':获取请求头签名(rk,requestId,timestamp)
        }
        nonce=随机字符串(16)
        timestamp=int(round(time.time() * 1000))
        
        param={
            "jsonId":jsonId,
            "timestamp":timestamp,
            "nonce":nonce,
            "signature":获取参数签名(nonce,timestamp)
        }
        async with session.get(url=url,params=param,headers=header) as response:
                res = await response.json()
                print(int(round(time.time() * 1000)),res)
                if(res['code']==0):
                    if(res['data']['status']==1):
                        print('抢奶成功')
                        sys.exit(0)
    except Exception as e:
        print("运行出错",e)

async def mn_time():
    
    url = 'https://mengniu-apig.xiaoyisz.com/mengniu-world-cup-1122/mp/public/api/timestamp'
    header={
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.30(0x18001e32) NetType/WIFI Language/zh_CN',
        'Referer':url,
        #'Authorization':Authorization
    }
    async with session.get(url=url,headers=header) as response:
            res = await response.json()
            print('服务器时间戳',res["data"],int(round(time.time() * 1000)))
            return int(res["data"])


async def 秒杀():
    while True:
        try:
            await 开抢()
        except Exception as e:
            print('发生异常', e)

async def 设置线程():
    Timers=Timer()
    #创建任务
    tasks = [asyncio.create_task(秒杀()) for i in range(work_count)]
    Timers.start()
    #开启任务
    #await mn_time()
    await asyncio.wait(tasks)



async def main():
    
    global rk 
    global session
    global context
    #调用js获取uuid
    with open('des.js', 'r', encoding='UTF-8') as f:
        js_code = f.read()
    context = execjs.compile(js_code)


    session=ClientSession()
    rk=await 获取RK()
    if rk is not None:
        await 查询中奖()
        #await mn_time()
        await 设置线程()
        
    await session.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
