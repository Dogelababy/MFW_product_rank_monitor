import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import pymysql 

password = input('输入数据库密码：')

db = pymysql.connect("localhost","root",password,"product_rank" )
cursor = db.cursor()

country_list=['日本','美国','泰国','马尔代夫','意大利','印度尼西亚','马来西亚','法国','澳大利亚','新西兰','越南','土耳其','斯里兰卡','新加坡','西班牙','加拿大','菲律宾','摩洛哥','瑞士','希腊','英国','奥地利','俄罗斯','芬兰','冰岛','捷克','毛里求斯','德国','斐济','阿联酋','肯尼亚','柬埔寨','塞尔维亚','葡萄牙','埃及','尼泊尔','墨西哥','荷兰','玻利维亚','阿根廷','克罗地亚','塞舌尔','印度','巴哈马','丹麦','缅甸','坦桑尼亚','挪威','纳米比亚','秘鲁','马达加斯加','以色列','智利','巴西','格鲁吉亚','古巴','老挝','南非','波兰','爱尔兰','瑞典','阿尔巴尼亚','乌拉圭','厄瓜多尔','斯洛文尼亚','突尼斯','波黑','匈牙利','伊朗','汤加','津巴布韦','约旦','瓦努阿图','比利时','哥斯达黎加','马耳他','哥伦比亚','爱沙尼亚']


for country in country_list:

    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    url = 'http://www.mafengwo.cn/sales/ajax_2017.php'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    params = {
        'act': 'GetContentList',
        '':'',
        'from': '',
        'kw':country,
        'to': '',
        'salesType': '28',
        'page': '1',
        'group': '1',
        'sort': 'smart',
        'sort_type': 'desc',
        'limit': '20'
    }

    content = requests.get(url,headers = headers, params = params)
    content.encoding = 'unicode_escape'

    soup = BeautifulSoup(content.text,"lxml")

    list_content = soup.find_all('a',class_='item clearfix')
    for i in range(len(list_content)):
        #获得商品名称
        product_name = list_content[i].find('h3').text[33:75]+'...'
        #获得店铺名称
        shop_name = list_content[i].find('span',class_='t').text[4:12]
        #获得商品ID
        product_id = str(list_content[i])[40:47]            
        #获得商品销量
        sales_record = list_content[i].find('p').text[2:5]
        #获得商品价格
        price = list_content[i].find('span',class_='price').text[:7]
        sql = "INSERT INTO PRODUCT_RANK_RECORD(query_time,country,product_rank,product_id,product_name,shop_name,sales_record,price)\
        VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"\
        %(nowTime,country,str(i+1),product_id,product_name,shop_name,sales_record,price)

        cursor.execute(sql)
        db.commit()
    print(country+'数据读取完毕,共'+str(len(list_content))+'条')