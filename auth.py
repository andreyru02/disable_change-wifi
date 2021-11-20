import requests


def authentication(inet_login, inet_password, mac):
    url = 'https://r.talakan.online/api.php?r=site/authorize'

    data = {
        "login": inet_login,
        "passwd": inet_password,
        "pathquery": f"https://r.talakan.online/guest/s/default/?ap=68:d7:9a:13:1d:99&id={mac}&&url=http://2.ru%2f"
                     f"&ssid=TalakanOnline"}

    print('Выполняется авторизация на TalakanOnline')
    with requests.Session() as s:
        resp = s.post(url, data).json()
        print(resp)
        if resp.get('success') is True:
            return True
        elif resp.get('error').get('detail')[0].get('code') == 'E002':
            return False
