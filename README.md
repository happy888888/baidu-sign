# baidu-Sign
百度贴吧签到，百度知道签到，百度知道打卡领取成长值和财富值，知道商城抽奖领取财富值
</br></br>

# 使用方式
* 1. fork本项目
* 2. 在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name为"cookie" （没有引号） value为以下三种形式之一(xxxxxxxxx需要替换)：
    *  2.1 ```BDUSS=xxxxxxxxx```
    *  2.2 ```BDUSS=xxxxxxxxx; STOKEN=xxxxxxxxx```
	*  2.3 
	
	       ```
	       BDUSS=xxxxxxxxx
	       BDUSS=xxxxxxxxx; STOKEN=xxxxxxxxx
	       BDUSS=xxxxxxxxx
	       ```
* 3 添加完"Secrets"后，点右上角'Star'即可首次运行,以后会每天上午10点运行
* 4 以后会每天早上8点自动运行


</br>
注：2.1形式只支持200个及以下贴吧数量的签到，2.2的形式支持200个以上贴吧(STOKEN必须有效，否则与2.1形式效果相同)，2.3形式用于多账户
