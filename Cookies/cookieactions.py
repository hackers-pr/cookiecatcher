import os, os.path, json

class cookieactions():

    def cookies_size(self):
        return str(round(os.path.getsize('Cookies/cookies.json')/1024))+' Kb'

    def number_of_cookies(self):

        with open('Cookies/cookies.json', 'r') as raw_cookies:
            cookies=json.loads(raw_cookies.read())
            return len(cookies)

    