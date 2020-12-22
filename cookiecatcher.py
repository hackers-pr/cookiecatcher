import requests, re, json, random, os
from time import sleep

class cookiecatcher():

    def __init__(self):
        self.next_page=None,
        self.STARTURLS=None,
        self.USERAGENT=None

    def configload(self):

        with open('config.json', 'r') as raw_config:
            config=json.loads(raw_config.read())
            USERAGENTS=config['const']['USERAGENTS']
            self.STARTURLS=config['const']['STARTURLS']
            self.next_page=random.choice(self.STARTURLS)
            self.USERAGENT=random.choice(USERAGENTS)
            self.SLOWDOWN=config['SLOWDOWN']
            self.SLOWDOWN_RANGE=config['SLOWDOWN_RANGE']

    def parsenext(self):
        print(self.next_page)
        dont_write=False; domain=self.next_page.split('/')[2]

        with open('Cookies/cookies.json', 'r') as raw_cookies:
            cookies=raw_cookies.read()
            current_cookies=json.loads(cookies)

            try:
                cookie=current_cookies[domain]
            except:
                cookie=None

        if cookie!=None:
            self.page=requests.get(self.next_page, headers={'user-agent': self.USERAGENT})
        else:
            self.page=requests.get(self.next_page, headers={'user-agent': self.USERAGENT, 'cookie': cookie})

        current_page=self.next_page
        res=re.findall('<a href="http[s]*://.*?"', self.page.text)

        if len(res)>0:
            self.next_page=random.choice([re.sub('<a href="(.+)"', r'\1', x) for x in res])
        else:
            print('Dead end, the next url will be selected from the STARTURLS')
            self.next_page=random.choice(self.STARTURLS)

        try:
            cookie=self.page.headers['set-cookie']
        except:
            dont_write=True

        if not dont_write:
            with open('Cookies/cookies.json', 'r') as raw_cookies:
                cookies=raw_cookies.read()
                old_cookies=json.loads(cookies); current_cookies=old_cookies

            with open('Cookies/cookies.json', 'w') as raw_cookies:
                current_cookies.update({domain: cookie})
                raw_cookies.write(json.dumps(current_cookies, indent=4))

        with open('Cookies/history.log', 'a') as history:
            history.write(current_page+'\n')

        if self.SLOWDOWN:
            sleep(random.randint(self.SLOWDOWN_RANGE[0], self.SLOWDOWN_RANGE[1]))

if __name__=="__main__":
    cc=cookiecatcher()
    cc.configload()
    while True:
        cc.parsenext()