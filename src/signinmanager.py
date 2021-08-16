import webbrowser, browser_cookie3, time, os, dill, multiprocessing
from src.apimanager import SearchApiManager

class SigninManager:
    _PATH = "/login"

    def __init__(self, chromepath, domain, cookie_probing_interval=5, cachedir='__cache__', authcache=None) -> None:
        self.domain = domain
        self.chromepath = chromepath
        self.cookie_probing_interval = cookie_probing_interval
        self._cachedir = cachedir
        self._shouldauthcache = authcache

    def get_cookies(self):
        if self._shouldauthcache:
            cookies = self.get_cache()
            if cookies is not None:
                print ('Getting cookies from cache')
                return cookies

        process = multiprocessing.Process(target=self._open_browser)
        process.start()
        print('Waiting for sign-in to complete')
        while True:
            cookies = browser_cookie3.chrome(domain_name=self.domain)
            if self.is_cookie_valid(cookies):
                print('Sign-in captured')
                self.write_cache(cookies)
                process.terminate()
                return cookies
            time.sleep(self.cookie_probing_interval)

    def write_cache(self, cookies):
        dir = self._cachedir
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(dir + "/" + 'cookies.pkl', 'wb') as f:
            f.write(dill.dumps(cookies))

    def get_cache(self):
        dir = self._cachedir
        try:
            with open(dir + "/" + 'cookies.pkl', 'rb') as f:
                res = f.read()
                return None if len(res) == 0 else dill.loads(res)
        except:
            return None

    def _open_browser(self):
        url = "https://" + self.domain + self._PATH
        chromedir = '"%s" %%s' % self.chromepath
        if webbrowser.get(chromedir).open_new_tab(url) == False:
            raise "Could not open chrome, possibly chrome isn't installed or 'chromepath' in config.ini is incorrect"
        print ("Opened chrome for sign-in")

    def is_cookie_valid(self, cookies):
        baseurl = "https://" + self.domain
        sm = SearchApiManager(baseurl, 'Art', cookies)
        try:
            res = sm.get(1, retry=1)
            return True
        except:
            return False
        

if __name__ == "__main__":
    sm = SigninManager()