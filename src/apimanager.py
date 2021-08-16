from src.cachemanager import ApiCacheManager

import requests, hashlib

class ApiManager:
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    def __init__(self, url, params, cookies, salt, cachedir='__cache__', shouldapicache=True):
        self._url = url
        self._url_params = params
        self._cookies = cookies
        self._salt = salt
        self._cachedir = cachedir
        self._shouldapicache = shouldapicache

    def get(self, proxy=None):
        self._url_params['sign'] = ApiManager._sign_params(self._url_params, self._salt)

        if self._shouldapicache:
            cached_response = ApiCacheManager.get_cache(self._cachedir, self._url_params['sign'])
            if cached_response is not None:
                return cached_response

        response = requests.get(self._url,                      \
                                headers=ApiManager._HEADERS,    \
                                params=self._url_params,        \
                                cookies=self._cookies,          \
                                proxies=proxy)

        json = response.json()
        if json['code'] == 0:
            ApiCacheManager.write_cache(self._cachedir, self._url_params['sign'], response.text)
        return json

    @classmethod
    def _sign_params(cls, params, salt):
        param_string = ""
        for key in sorted(list(params.keys())):
            if params[key] not in [None, "", []]:                    
                param_string += key + (key if type(params[key]) == list else str(params[key]))
        return hashlib.md5((param_string + salt).encode('utf-8')).hexdigest()

class DailyFansApiManager(ApiManager):
    _PATH = '/v/api/author/daily_fans/'

    def __init__(self, url, authorid, cookies, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorid
        params = {
            'author_id': authorid
        }
        salt = 'daily_fans' + authorid
        super().__init__(url+self._PATH, params, cookies, salt, cachedir=cachedir, shouldapicache=shouldapicache)

    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                res = super().get(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Daily fans response invalid for page {self._authorid} ', res)
                return res
            except Exception as e:
                print(f'Exception occured fetching daily fans for {self._authorid}: ', e)
        raise Exception(f'All {retry} retries exhaused for author dailt fans {self._authorid}')

class AudienceDistributionApiManager(ApiManager):
    _PATH = '/v/api/author/audience_distribution_info/'

    def __init__(self, url, authorid, cookies, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorid
        params = {
            'author_id': authorid
        }
        salt = 'audience_distribution_info' + authorid
        super().__init__(url+self._PATH, params, cookies, salt, cachedir=cachedir, shouldapicache=shouldapicache)

    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                res = super().get(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Audience Distribution response invalid for author {self._authorid} ', res)
                return res
            except Exception as e:
                print(f'Exception occured fetching audience_distribution_info for {self._authorid}: ', e)
        raise Exception(f'All {retry} retries exhaused for author audience_distribution_info {self._authorid}')

class CoreMetricsApiManager(ApiManager):
    _PATH = '/v/api/author/audience_action_info/'

    def __init__(self, url, authorid, cookies, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorid
        params = {
            'author_id': authorid
        }
        salt = 'core_metrics' + authorid
        super().__init__(url+self._PATH, params, cookies, salt, cachedir=cachedir, shouldapicache=shouldapicache)

    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                res = super().get(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Core metrics response invalid for author {self._authorid} ', res)
                return res
            except Exception as e:
                print(f'Exception occured fetching core metrics for {self._authorid}: ', e)
        raise Exception(f'All {retry} retries exhaused for author core metrics {self._authorid}')

class TrendingVideosApiManager(ApiManager):
    _PATH = '/v/api/author/recent_item_info/'

    def __init__(self, url, authorid, cookies, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorid
        params = {
            'author_id': authorid
        }
        salt = 'trending_videos' + authorid
        super().__init__(url+self._PATH, params, cookies, salt, cachedir=cachedir, shouldapicache=shouldapicache)

    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                res = super().get(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Trending videos response invalid for author {self._authorid} ', res)
                return res
            except Exception as e:
                print(f'Exception occured fetching trending videos for {self._authorid}: ', e)
        raise Exception(f'All {retry} retries exhaused for author trending videos {self._authorid}')

class SearchApiManager(ApiManager):
    _PATH = '/h/api/gateway/handler_get'
    SALT = 'c040a11e10d42f8205a267904f49c5bd'

    def __init__(self, url, topic, cookies, country=None, cachedir='__cache__', shouldapicache=True):
        search_params = {
            'page': 1,
            'limit': 20,
            'sort_field': 'comp_rank', 
            'sort_type': 2,
            'author_topic': topic,
            'service_name': 'search.AdTcmSearchService',
            'service_method': 'AuthorPlazaSearch'
        }
        if country is not None:
            search_params['author_region'] = country
        super().__init__(url+self._PATH, search_params, cookies, SearchApiManager.SALT, cachedir=cachedir, shouldapicache=shouldapicache)

    def get(self, page=1, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        self._url_params['page'] = page
        while retry>0:
            retry-=1
            try:
                res = super().get(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Search response invalid for page {page} ', res)
                return res
            except Exception as e:
                sign = self._url_params['sign']
                print(f'Exception occured with page {page}, sign {sign}: ', e)
        raise Exception(f'All {retry} retries exhaused for page {page}')

class RelatedCreatorApimanager:
    PATH = '/h/api/gateway/handler_get/'
    SALT = 'bcabc7954431b53e2d3ca133f21b9a9a'

    def __init__(self, url, authorid, cookies, cachedir='__cache__', shouldapicache=True):
        self._authorid = authorid
        self._url = f'{url}{self.PATH}?author_ids=["{authorid}"]&req_source=0&service_name=search.AdTcmSearchService' + \
                    f'&service_method=SimilarCreatorsSearch&sign=bcabc7954431b53e2d3ca133f21b9a9a'
        self._cookies = cookies
        self._cachedir = cachedir
        self._shouldapicache = shouldapicache

    def execute(self, proxy=None):
        if self._shouldapicache:
            cached_response = ApiCacheManager.get_cache(self._cachedir, self.SALT+self._authorid)
            if cached_response is not None:
                return cached_response

        response = requests.get(self._url,                      \
                                headers=ApiManager._HEADERS,    \
                                cookies=self._cookies,          \
                                proxies=proxy)

        json = response.json()
        if json['code'] == 0:
            ApiCacheManager.write_cache(self._cachedir, self.SALT+self._authorid, response.text)
        return json

    def get(self, proxyManager=None, retry=5):
        proxy = proxyManager.next() if proxyManager is not None else None
        while retry>0:
            retry-=1
            try:
                res = self.execute(proxy)
                if res['code'] != 0:
                    self._shouldapicache = False
                    raise Exception(f'Related creator response invalid for  ', res)
                return res
            except Exception as e:
                sign = self.SALT
                print(f'Exception occured fetching related creators for author {self._authorid}, sign {sign}: ', e)
        raise Exception(f'All {retry} retries exhaused fetching related creators for author {self._authorid}')

if __name__ == "__main__":
    sm = ApiManager()


''' hasher js for future reference
"2e5b": function(e, t, n) {
        "use strict";
        n.d(t, "a", function() {
            return f
        });
        n("caad"),
        n("a15b"),
        n("d81d"),
        n("b64b");
        var a = n("f3f3")
          , r = n("0122")
          , i = n("6821")
          , o = n.n(i)
          , c = "c040a11e10d42f8205a267904f49c5bd";
        function s(e) {
            return void 0 === e || null === e
        }
        function u(e) {
            return ["string", "number"].includes(Object(r["a"])(e))
        }
        function d(e) {
            return Array.isArray(e)
        }
        function l(e) {
            var t = Object.keys(e).sort().map(function(t) {
                var n = e[t];
                return s(n) ? "" : t + (u(n) ? n : t)
            }).join("");
            return o()(t + c)
        }
        function p(e) {
            if (!e || "object" !== Object(r["a"])(e))
                return e;
            for (var t = {}, n = 0, a = Object.keys(e); n < a.length; n++) {
                var i = a[n]
                  , o = e[i];
                t[i] = d(o) ? JSON.stringify(o) : o
            }
            return t
        }
        function f(e, t, n, r, i) {
            var o = {
                service_name: e,
                service_method: t,
                sign_strict: r ? 1 : void 0
            };
            return Object(a["a"])(Object(a["a"])(Object(a["a"])({}, i ? p(n) : n), o), {}, {
                sign: l(Object(a["a"])(Object(a["a"])({}, n), o))
            })
        }
    },
'''