# -*- coding: utf-8 -*-
import requests
import json
import hashlib
import re

class baiduTool():
    "百度贴吧、知道签到类"
    def __init__(self, cookieData):
        "验证登录cookie"
        #创建session
        self.__session = requests.session()
        #添加cookie
        requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookieData)
        #设置header
        self.__session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36","Referer":"https://www.baidu.com/"})
        #设置重试次数
        retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.__session.mount('http://', retry)
        self.__session.mount('https://', retry)

        try:
            content = self.__session.get("http://tieba.baidu.com/dc/common/tbs")
        except:
            raise Exception("登录验证异常")
        data = json.loads(content.text)
        if(data["is_login"] == 0):
            raise Exception("登录失败,cookie异常")
        self.__tbs = data["tbs"]
        self.name = self.getLoginInfo()["userName"]

        try:
            self.getUserInfo()
        except:
            self.getTiebaLike = self.getTiebaLikeX
        else:
            self.getTiebaLike = self.getTiebaLikeG
    
    def getTiebaLikeX(self):
        "获取关注的贴吧列表(贴吧数量<=200时使用这个函数获取贴吧列表)"
        content = self.__session.get("https://tieba.baidu.com/mo/q/newmoindex")
        data = json.loads(content.text)
        if(data["no"] == 0):
            return [x["forum_name"] for x in data["data"]["like_forum"]]
        else:
            return []

    def getTiebaLikeG(self):
        "获取关注的贴吧列表迭代器(贴吧数量>200时使用这个函数获取贴吧列表，需要stoken)"
        content = self.__session.get("http://tieba.baidu.com/f/like/mylike?&pn=1", timeout=(5, 20))

        #获取页面数,每页有20个贴吧
        tpn = int(re.match('.*\/f\/like\/mylike\?&pn=(.*?)\"\>尾页.*', content.text, re.S|re.I).group(1))

        tp = 1 #当前页面
        #编译正则表达式
        pattern = re.compile('.*?\<a href=\"\/f\?kw=.*?title=\"(.*?)\"\>')
        while (tp <= tpn):
            #获取当前页面贴吧名称数组
            tbname = pattern.findall(content.text)
            for x in tbname:
                yield x

            #获取下一页面
            tp += 1
            content = self.__session.get(f"http://tieba.baidu.com/f/like/mylike?&pn={tp}", timeout=(5, 20))

    def getLoginInfo(self):
        "获取登录信息"
        return self.__session.get("https://zhidao.baidu.com/api/loginInfo",).json()

    def getUserInfo(self):
        "获取用户信息(需要stoken)"
        return self.__session.get("https://tieba.baidu.com/f/user/json_userinfo", allow_redirects=False).json()

    def tiebaSign(self, name):
        "签到指定贴吧"
        md5 = hashlib.md5(f'kw={name}tbs={self.__tbs}tiebaclient!!!'.encode('utf-8')).hexdigest()
        data = {
            "kw": name,
            "tbs": self.__tbs,
            "sign": md5
            }
        #构造签到数据包，客户端有对参数加了md5验证
        content = self.__session.post("http://c.tieba.baidu.com/c/c/forum/sign", data=data)
        data = json.loads(content.text)
        if(data["error_code"] == '0'):
            return {"code":0,"info":f'获得经验:{data["user_info"]["sign_bonus_point"]}  已连续签到{data["user_info"]["cont_sign_num"]}天'}
        else:
            return {"code":int(data["error_code"]),"info":data["error_msg"]}

    def zhidaoSign(self):
        "签到百度知道"
        content = self.__session.get("https://zhidao.baidu.com/")
        stoken = re.match('.*stoken\":\"(.*?)\".*', content.text, re.S|re.I).group(1)
        #这个stoken与cookie里面的stoken不是一个东西
        data = {
            "cm": "100509",
            "utdata": "91%2C91%2C106%2C97%2C97%2C102%2C98%2C91%2C99%2C103%2C97%2C100%2C126%2C106%2C100%2C102%2C15823570069820",
            "stoken": stoken
            }
        content = self.__session.post("https://zhidao.baidu.com/submit/user", data=data)
        data = json.loads(content.text)
        if(data["errorNo"] == 0):
            return {"code":0,"info":"签到成功"}
        else:
            return {"code":data["errorNo"],"info":data["errorMsg"]}

    def zhidaoTask(self, taskId: int):
        "百度知道任务领取"
        content = self.__session.get("https://zhidao.baidu.com/")
        stoken = re.match('.*stoken\":\"(.*?)\".*', content.text, re.S|re.I).group(1)
        data = {
            "taskId": taskId,
            "stoken": stoken
            }
        content = self.__session.post("https://zhidao.baidu.com/task/submit/getreward", data=data, timeout=(5, 20))
        data = json.loads(content.text)
        return {"code":data["errno"],"info":data["errmsg"]}

    def zhidaoShopLottery(self):
        "百度知道商城免费抽奖"
        content = self.__session.get("https://zhidao.baidu.com/shop/lottery")
        luckytoken = re.match('.*luckyToken\', \'(.*?)\'.*', content.text, re.S|re.I).group(1)
        #获取luckytoken用于抽奖
        content = self.__session.get(f"https://zhidao.baidu.com/shop/submit/lottery?type=0&token={luckytoken}")
        #type取0是免费抽奖，取1是50财富抽一次，取2是连抽十次

        data = json.loads(content.text)
        if(data["errno"] == 0):
            return {"code":0,"info":data["data"]["prizeList"][0]["name"]}
        #注意prizeList是一个数组，免费抽奖是单抽所以取0，知道商城还有个十连抽
        else:
            return {"code":data["errno"],"info":data["errmsg"]}
