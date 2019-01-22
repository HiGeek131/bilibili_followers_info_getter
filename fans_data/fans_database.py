# 使用前需要先把浏览器该API的cookies参数给拷贝到目录下的cookie.txt文件内

import requests
import time

user_id = 4893237   # 你的uid
api_url = "http://api.bilibili.com/x/relation/followers"    # 傻屌死妈逼站的粉丝数据API接口URL
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"}     # 浏览器包头字典文件，可以不用改也可以自己尝试使用自己的浏览器报文文件
manual_cookies = {}     # 先创建一个用于cookie的空字典

session = requests.session()    # 创建一个会话
with open("cookies.txt", 'r', encoding='utf-8') as cookie_file:  # 打开同目录下的cookie.txt文件，读取cookie参数
    cookies_txt = cookie_file.read().strip(';')  # 去头去尾，其实没啥屌用，只是防止你的格式不规范
    for item in cookies_txt.split(';'):  # 用";"来把txt的文本分割成字典组
        name, value = item.strip().split('=', 1)  # 然后再用"="来把字典组分割成名字与参数
        manual_cookies[name] = value  # 把参数复制到字典

cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)  # 格式化成什么鬼jar文件，大概是java数据吧。这句我是从网上查的，我也不懂
session.cookies = cookiesJar  # 把格式化后的cookie放入会话


def require_followers(uid, pn):  # uid和页数，一页有50个用户参数和其他奇奇怪怪的东西，自己慢慢找
    params = {"vmid": uid, "pn": pn}  # 参数字典
    fans_info = session.get(url=api_url, params=params).json()  # get请求，然后json反序列化
    return fans_info  # 返回参数


def main():
    fans_info = require_followers(user_id, 1)  # 暂时先获取一次，因为需要知道我有多少个粉丝，然后取整加一就是我粉丝页数。但是屁用没有，傻逼逼哩逼哩限制了API。
    fans_num = fans_info["data"]["total"]  # 这个是你的粉丝数参数
    pages = fans_num//50+1  # 取整加一是最大的页数
    for i in range(pages):  # 遍历页数
        fans_info = require_followers(user_id, i)  # get请求
        print(str(i) + str(fans_info))  # 这是我测试debug用的语句，就是显示获取到的数据，没有做可视化，非常乱，你就凑合着试试吧
        # time.sleep(0.1)  # 延时，防止速度过快被逼哩逼哩BAN掉你的IP。其实没这个必要，因为bilibili貌似没有限制，我以前做爬虫一秒钟请求了同API几千次都没事。


if __name__ == '__main__':
    main()  # 运行main() （傻子都知道是什么意思我在这解释干嘛。。）
