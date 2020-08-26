import os,time
from baiduTool import baiduTool

def cookie2dict(cookies):
    res = {}
    arr = cookies.split(';')
    for x in arr:
        key, value = x.split('=')
        if key.strip().upper() == 'BDUSS':
            res["BDUSS"] = value.strip()
        elif key.strip().upper() == 'STOKEN':
            res["STOKEN"] = value.strip()
    return res

def shopLottery(bd):
    "知道商城抽奖"
    #一天可以抽两次，间隔大于10分钟，最好别在凌晨抽
    try:
        lott = bd.zhidaoShopLottery()
    except Exception as e:
        print(f'{bd.name} 知道商城抽奖异常,原因({str(e)})')
    else:
        print(f'{bd.name} 知道商城抽奖信息：{lott["info"]}')

def signTieba(bd):
    "签到贴吧和知道"

    print(f'开始为用户({bd.name})签到百度知道，百度知道，知道商城抽奖')
    
    #开始贴吧签到
    ii=0
    jj=0
    try:
        tb = bd.getTiebaLike()
    except Exception as e:
        print(f'贴吧签到异常,原因({str(e)})，跳过贴吧签到')
    else:
        for x in tb:
            ii += 1
            try:
                re = t.tiebaSign(x)
            except Exception as e:
                print(f'贴吧 {x} 签到异常,原因{str(e)}')
            else:
                print(f'贴吧 {x:<{26-len(x.encode("GBK"))+len(x)}} 签到信息：{re["info"]}')
                if re["code"] == 0:
                    jj += 1

    print(f'一共{ii}个贴吧，成功签到{jj}个')

    try:
        zd = bd.zhidaoSign()
    except Exception as e:
        print(f'百度知道签到异常,原因({str(e)})')
    else:
        print(f'百度知道签到信息：{zd["info"]}')

    #下面是百度知道打卡任务
    try:
        zd = bd.zhidaoTask(176) #打卡任务id为176
    except Exception as e:
        print(f'百度知道打卡任务异常,原因({str(e)})')
    else:
        print(f'百度知道打卡任务信息：{zd["info"]}')

def main():
    cookies = os.environ.get("cookie")
    arr = cookies.split('\n')
    bds = []
    ii = 0
    for x in arr:
        ii += 1
        try:
            bd = baiduTool(cookie2dict(x))
            bds.append(bd)
        except Exception as e:
            print(f'第{ii}个账户登录异常,原因({str(e)})，跳过此账户的所有签到')

    for x in bds:
        shopLottery(x)

    next_time = int(time.time()) + 600

    for x in bds:
        signTieba(x)

    delay = next_time - int(time.time())
    if delay > 0:
        print(f'等待{delay}秒后再次进行知道商城抽奖')
        time.sleep(delay)

    for x in bds:
        shopLottery(x)


__name__ == '__main__' and main()
