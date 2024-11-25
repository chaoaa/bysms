import  requests,pprint

payload = {
        'username': 'lin',
        'password': '88888888'
    }

response = requests.post("http://localhost/api/mgr/signin",
                             data=payload)

retDict = response.json()

sessionid = response.cookies['sessionid']

# 再发送列出请求，注意多了 keywords
payload = {
    'action': 'list_medicine',
    'pagenum': 1,
    'pagesize' : 3,
    'keywords' : '抗 清'
}

response = requests.get('http://localhost/api/mgr/medicines',
              params=payload,
              cookies={'sessionid': sessionid})

pprint.pprint(response.json())