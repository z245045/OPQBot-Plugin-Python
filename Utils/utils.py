import json
import re
import requests

token = ""
cjx_key = ''
xzys_key= ''

def get_nmsl():
    url = 'https://nmsl.shadiao.app/api.php?from=' + token
    res = requests.get(url=url).text
    return res


def get_nmsl_max():
    url = 'https://nmsl.shadiao.app/api.php?level=max&from=' + token
    res = requests.get(url=url).text
    return res


def get_chp():
    url = 'https://chp.shadiao.app/api.php?from=' + token
    res = requests.get(url=url).text
    return res


def get_pyq():
    url = 'https://pyq.shadiao.app/api.php?from=' + token
    res = requests.get(url=url).text
    return res


def get_djt():
    url = 'https://du.shadiao.app/api.php?from=' + token
    res = requests.get(url=url).text
    return res


def get_cjx(msg):
    QQ = msg.FromQQ
    url = 'http://japi.juhe.cn/qqevaluate/qq?key='+ cjx_key + '&qq='+str(QQ)
    res = requests.get(url=url)
    result = json.loads(res.text)
    conclusion = result['result']['data']['conclusion']
    analysis = result['result']['data']['analysis']
    text = '被测QQ号：'+str(QQ)+'\r\n\r\n' + '测试结论：' + conclusion + '\r\n\r\n' + '结果分析：' + analysis + ""
    return text


def get_xzys(xing_zuo, dtype):
    if dtype == '今日':
        type = 'today'
    elif dtype == '明日':
        type = 'tomorrow'
    elif dtype == '周':
        type = 'week'
    elif dtype == '月':
        type = 'month'
    elif dtype == '年':
        type = 'year'
    else:
        return "使用说明：请输入**座今日/明日/周/月/年运势（例如：狮子座今日运势、狮子座周运势等）"
    url = 'http://web.juhe.cn:8080/constellation/getAll'
    params = {
        'key': xzys_key,
        'consName': xing_zuo,
        'type': type
    }
    res = requests.get(url=url,params=params)
    result = json.loads(res.text)
    if dtype == '今日' or dtype == '明日':
        text = '星座名称: ' + result['name'] + '\r\n\r\n' + '日期: ' + result['datetime'] + '\r\n\r\n' + \
               '综合指数: ' + result['all'] + '\r\n\r\n' + '健康指数: ' + result['health'] + '\r\n\r\n' + \
               '爱情指数: ' + result['love'] + '\r\n\r\n' + '财运指数: ' + result['money'] + '\r\n\r\n' + \
               '工作指数: ' + result['work'] + '\r\n\r\n' +'幸运色: ' + result['color'] + '\r\n\r\n' + \
               '幸运数字: ' + str(result['number']) + '\r\n\r\n'+ '概述: ' + result['summary']
    elif dtype == '周':
        text = '星座名称: ' + result['name'] + '\r\n\r\n' + '日期: ' + result['date'] + '\r\n\r\n' + \
               '学业/求职: ' + result['job'] + '\r\n\r\n' + '爱情: ' + result['love'] + '\r\n\r\n' + \
               '财运: ' + result['money'] + '\r\n\r\n' + '工作: ' + result['work'] + '\r\n\r\n'
    elif dtype == '月':
        text = '星座名称: ' + result['name'] + '\r\n\r\n'+ '日期: ' + result['date'] + '\r\n\r\n' + result['all'] + '\r\n\r\n' + \
               result['health'] + '\r\n\r\n' + result['love'] + '\r\n\r\n' + result['money'] + '\r\n\r\n' + \
               result['work']
    elif dtype == '年':
        text = '星座名称: ' + result['name'] + '\r\n\r\n'+ '日期: ' + result['date'] + '\r\n\r\n' + \
               '年度密码:①概述: ' + result['mima']['info'] + '\r\n' + '②说明: ' + result['mima']['text'][0]+ '\r\n\r\n' + \
               result['career'][0] + '\r\n\r\n' + result['love'][0] + '\r\n\r\n' + result['health'][0] + '\r\n\r\n' + \
               result['finance'][0]
    print(res.text)
    return text


def get_comment():
    res = requests.get('https://www.mouse123.cn/api/163/api.php').json()
    text = res['comment_content']
    return text


if __name__ == '__main__':
    pattern = re.compile(r'#(.*?座)(.*?)运势')
    m = pattern.match("#白羊座今日运势")
    if m is not None:
        get_xzys(m.group(1), m.group(2))
    else:
        print("参数错误")
