import requests
import sys
from lxml import etree
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import SendMsg

sched = BackgroundScheduler()
def getContent(url):
    res = requests.get(url)
    return res.content


def save(url,city):
    company_names = list()
    company_names_links = list()
    update_times = list()


    html = etree.HTML(getContent(url))
    con = html.xpath('//div[@class="jobList"]//tbody[@id="tb_job_list"]//tr[@class="tr_list"]')
    for e in con:
        company_names =  e.xpath('//td/a//text()')
        company_names_links =  e.xpath("//td/a//@href")
        update_times = e.xpath('//td[@class="cols2"]//text()')


    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    sendMsg(company_names,company_names_links,update_times)

    with open(city+'info.txt','a+') as f:

        for idx,name in enumerate(company_names):
            if now_time == update_times[idx]:
                f.write("".join(company_names[idx]) + "\t" 
                        + "http://www.yingjiesheng.com"+"".join(company_names_links[idx]) + "\t"
                        + "".join(update_times[idx]) +'\n')


def sendMsg(company_names,company_names_links,update_times):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    data = "# "+now_time+"招聘信息\n"

    for idx,name in enumerate(company_names):
        if now_time == update_times[idx]:
            v= "- "+"".join(company_names[idx]) + "\t"  + "http://www.yingjiesheng.com"+"".join(company_names_links[idx]) + "\t"  + "".join(update_times[idx]) +'\n'

            data+=v
    SendMsg.send(data)


def scheduleTask():

    arr = {'nanjing':'http://www.yingjiesheng.com/zhuanye/jisuanji/nanjing/list_1.html',
            #'suzhou':'http://www.yingjiesheng.com/zhuanye/jisuanji/suzhou/',
            #'jiangsu':'http://www.yingjiesheng.com/zhuanye/jisuanji/jiangsu/'
            }

    for city in arr:
        save(arr[city],city)

if __name__ == "__main__":



    #表示每隔3天17时19分07秒执行一次任务
    sched.add_job(scheduleTask, 'interval',id='douban_job',days  = 0,hours = 0,minutes = 0,seconds = 10)
    sched.start()
    index = 0 #0
    while True:
        print(index)
        time.sleep(1)
        if(index % 86400 == 0 and index != 0):
            print("招聘爬虫服务正常稳定运行" + str(int(index / 86400)) + "天")
        index += 1

    




