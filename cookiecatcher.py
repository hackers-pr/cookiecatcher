import requests, re, json, random
from time import sleep
from Cookies import cookieactions

class cookiecatcher():

    def configload(self):

        with open('config.json', 'r') as raw_config:
            config=json.loads(raw_config.read())
            USERAGENTS=config['const']['USERAGENTS']
            self.STARTURLS=config['const']['STARTURLS']
            self.next_page=random.choice(self.STARTURLS)
            self.USERAGENT=random.choice(USERAGENTS)
            self.SLOWDOWN=config['SLOWDOWN']
            self.SLOWDOWN_RANGE=config['SLOWDOWN_RANGE']
            self.CONTINUE_MESSAGE_X=config['CONTINUE_MESSAGE_X']

    def request(self):
        self.domain=re.sub(r'[?]', '/', self.next_page).split('/')[2]
        self.current_page=self.next_page

        with open('Cookies/cookies.json', 'r') as raw_cookies:
            cookies=raw_cookies.read()
            current_cookies=json.loads(cookies)

            if not current_cookies.get(self.domain) is None:
                cookie=current_cookies[self.domain]
            else:
                cookie=None

        try:
            if not cookie is None:
                self.page=requests.get(self.next_page, headers={'user-agent': self.USERAGENT}, timeout=5)
            else:
                self.page=requests.get(self.next_page, headers={'user-agent': self.USERAGENT, 'cookie': cookie}, timeout=5)

        except:
            self.next_page=random.choice(self.STARTURLS)

    def parse(self):
        print(self.next_page)
        dont_write=False

        res=[re.sub('<a href="(http[s]*://.+)"', r'\1', raw_url) for raw_url in re.findall('<a href="http[s]*://.*?"', self.page.text)]

        while res.count(self.current_page)!=0:
            res.remove(self.current_page)

        if len(res)>0:
            self.next_page=random.choice([re.sub('<a href="(.+)"', r'\1', x) for x in res])
        else:
            self.next_page=random.choice(self.STARTURLS)

        if not self.page.headers.get('set-cookie') is None:
            cookie=self.page.headers['set-cookie']
        else:
            dont_write=True

        if not dont_write:
            with open('Cookies/cookies.json', 'r') as raw_cookies:
                cookies=raw_cookies.read()
                old_cookies=json.loads(cookies); current_cookies=old_cookies

            with open('Cookies/cookies.json', 'w') as raw_cookies:
                current_cookies.update({self.domain: cookie})
                raw_cookies.write(json.dumps(current_cookies, indent=4))

        with open('Cookies/history.log', 'a') as history:
            history.write(self.current_page+'\n')

        if self.SLOWDOWN:
            sleep(random.randint(self.SLOWDOWN_RANGE[0], self.SLOWDOWN_RANGE[1]))

if __name__=="__main__":
    cc=cookiecatcher()
    user_input=str()
    cc.configload()

    while user_input.lower().strip()!='q':

        for unused in range(cc.CONTINUE_MESSAGE_X):
            cc.request()
            cc.parse()

        user_input=input('Cookies ('+str(cookieactions.cookieactions().number_of_cookies())+') take '+str(cookieactions.cookieactions().cookies_size())+' of memory. Continue? (q to quit)\n')
