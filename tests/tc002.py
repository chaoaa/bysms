import  requests,pprint

# 先登陆,获取sessionid
payload = {
        'username': 'lin',
        'password': '88888888'
    }

response = requests.post("http://localhost/api/mgr/signin",
                             data=payload)

retDict = response.json()
print(response.cookies)
sessionid = response.cookies['sessionid']

# 再发送列出请求，注意多了 pagenum 和 pagesize
payload = {
    'action': 'list_medicine',
    'pagenum': 1,
    'pagesize' : 3
}

response = requests.get('http://localhost/api/mgr/medicines',
              params=payload,
              cookies={'sessionid': sessionid})

pprint.pprint(response.json())