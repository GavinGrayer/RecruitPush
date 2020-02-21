import requests
import json


def send(msg):
    data1 = {
    "appToken":"AT_XXXXXXXXXXXXXXXXXXXX",
    "content":msg,
    "contentType":3,
    "uids":getUsers(),
    #"url":"http://wxpusher.zjiecode.com"
    }

    headers = {
        "Content-Type": "application/json"
    }


    res = requests.post('http://wxpusher.zjiecode.com/api/send/message/',
        headers=headers,data=json.dumps(data1))

    print(res.text)


# requests.get('http://wxpusher.zjiecode.com/api/send/message/'+
#         '?appToken=AT_8DIx3TyiEuSiuGBjhDkzWW2okxjhB17o'
#         +'&content=123'
#         +'&uid=UID_04D756TbOIavqrY3FMsaXeOTWfb9')

# print(res1.content)

#msg = "# hello \n" + "## hello2 \n" + '- 1\n' + '- 2\n'
#send(msg)

def getUsers():
    uids = list()
    res = requests.get('http://wxpusher.zjiecode.com/api/fun/wxuser?appToken=AT_XXXXXXXXXXXXXXXXXXXX'
    +'&page=0&pageSize=10' )
    data = json.loads(res.content.decode())
    for name in data['data']['records']:
        uids.append(name['uid'])

    print(uids)
    return uids

getUsers()