from src.cachemanager import ApiCacheManager

import subprocess, random, string

class TiktokScrapperManager:
    def __init__(self, authorhandle, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorhandle
        self._cachedir = cachedir
        self._shouldapicache = shouldapicache
        self._filename = f'video_metadata_{authorhandle}'
        self._session = ''.join(random.choice(string.ascii_lowercase) for x in range(32))
        self._scraper_cmd = f'tiktok-scraper user {self._authorid} -n 0 -t json -f {self._filename} --filepath {self._cachedir} --session {self._session}'

    def execute(self, proxy=None):
        if self._shouldapicache:
            cached_response = ApiCacheManager.get_cache(self._cachedir, self._filename)
            if cached_response is not None:
                return cached_response

        p = subprocess.Popen(self._scraper_cmd, shell=True)
        p.wait()
        json = ApiCacheManager.get_cache(self._cachedir, self._filename)
        return json
    
    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next()['https'] if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                return self.execute(proxy)
            except Exception as e:
                print(f'Exception occured fetching video metadata for author {self._authorid}: ', e)
        raise Exception(f'All {retry} retries exhaused fetching video metadata for author {self._authorid}')

if __name__ == "__main__":
    m = TiktokScrapperManager('colinwasson', shouldapicache=False)
    print(m.get())