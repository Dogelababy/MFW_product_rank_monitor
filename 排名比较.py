import pymysql 
from prettytable import PrettyTable
country_list=['日本','美国','泰国','马尔代夫','意大利','印度尼西亚','马来西亚','法国','澳大利亚','新西兰','越南','土耳其','斯里兰卡','新加坡','西班牙','加拿大','菲律宾','摩洛哥','瑞士','希腊','英国','奥地利','俄罗斯','芬兰','冰岛','捷克','毛里求斯','德国','斐济','阿联酋','肯尼亚','柬埔寨','塞尔维亚','葡萄牙','埃及','尼泊尔','墨西哥','荷兰','玻利维亚','阿根廷','克罗地亚','塞舌尔','印度','巴哈马','丹麦','缅甸','坦桑尼亚','挪威','纳米比亚','秘鲁','马达加斯加','以色列','智利','巴西','格鲁吉亚','古巴','老挝','南非','波兰','爱尔兰','瑞典','阿尔巴尼亚','乌拉圭','厄瓜多尔','斯洛文尼亚','突尼斯','波黑','匈牙利','伊朗','汤加','津巴布韦','约旦','瓦努阿图','比利时','哥斯达黎加','马耳他','哥伦比亚','爱沙尼亚']

while True:
    country = input('输入查询国家：')
    if country in country_list:
        print('===========================')
        db = pymysql.connect("localhost","root","*****","product_rank" )
        cursor = db.cursor()
        sql = "SELECT DISTINCT query_time FROM PRODUCT_RANK_RECORD WHERE country = '%s'"%(country)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(country+'的查询记录有'+str(len(results))+'条\n查询时间分别是：')

        try:
            for i in range(len(results)):
                print('记录'+str(i+1)+':'+results[i][0])
        except:
            print('暂无记录')

        rank_dict1={}
        rank_dict2={}    
        index1 = int(input('请输入需要比对的第一个日期的记录序号：'))
        query_time_1 = results[index1-1][0]
        # print(query_time_1)
        index2 = int(input('请输入需要比对的第二个日期的记录序号：'))
        query_time_2 = results[index2-1][0]
        # print(query_time_2)

        sql1 = "SELECT product_rank, product_id, shop_name FROM PRODUCT_RANK_RECORD\
            WHERE country = '%s' AND query_time = '%s'"%(country,query_time_1)
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        for i in results1:
            rank_dict1[i[1]]=i[0]

        sql2 = "SELECT product_rank, product_id, shop_name FROM PRODUCT_RANK_RECORD\
            WHERE country = '%s' AND query_time = '%s'"%(country,query_time_2)
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        for i in results2:
            rank_dict2[i[1]]=i[0]

        all_results = []

        for i in range(len(results2)):
            all_results.append(list(results1[i])+list(results2[i]))
            try:
                all_results[i].append(int(rank_dict1[results2[i][1]])-int(rank_dict2[results2[i][1]]))
            except:
                all_results[i].append('新上榜')

        table = PrettyTable(['时间1的排序','时间1的商品ID','时间1的商家名称','时间2的排序','时间2的商品ID','时间2的商家名称','排名变化'])
        for row in all_results:
            table.add_row(row)
        print('========================================================================')    
        print(country+'  '+query_time_1+' 的 TOP20  VS  '+query_time_2+' 的 TOP20')
        print('========================================================================')    
        print(table)
    else:
        break
