from multiprocessing import Pool
from src.apimanager import CoreMetricsApiManager, DailyFansApiManager, RelatedCreatorApimanager, SearchApiManager, AudienceDistributionApiManager, TrendingVideosApiManager
from src.tiktokscrapermanager import TiktokScrapperManager

import math, concurrent.futures, sys

class SearchDispatcher:
    @classmethod
    def dispatch(cls, baseurl, proxyManager, topic, cookies, country=None, maxnum = sys.maxsize, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        repository = {}
        print('Fetching page 1 of search')
        sm = SearchApiManager(baseurl,                          \
                        topic,                                  \
                        cookies,                                \
                        country=country,                        \
                        cachedir=cachedir,                      \
                        shouldapicache=shouldapicache)
        resp1 = sm.get(1, proxyManager)
        SearchDispatcher._append_repo(repository, resp1)

        limit = resp1['data']['pagination']['limit']
        total_count = min(int(maxnum), resp1['data']['pagination']['total_count']) + limit
        num_pages = math.ceil(total_count/limit)

        print(f'Dispatching thread pool to request {num_pages} search pages with {total_count} authors')
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for page in range(2, num_pages+1):
                smt = SearchApiManager(baseurl,                 \
                        topic,                                  \
                        cookies,                                \
                        country=country,                        \
                        cachedir=cachedir,                      \
                        shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        smt.get, page=page, proxyManager=proxyManager
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                SearchDispatcher._append_repo(repository, response)

            SearchDispatcher.fetch_audience_distribution(repository, baseurl, proxyManager, cookies, parallelthreadcount, cachedir, shouldapicache)
            SearchDispatcher.fetch_core_metrics(repository, baseurl, proxyManager, cookies, parallelthreadcount, cachedir, shouldapicache)
            SearchDispatcher.fetch_trending_videos(repository, baseurl, proxyManager, cookies, parallelthreadcount, cachedir, shouldapicache)
            SearchDispatcher.fetch_daily_fans(repository, baseurl, proxyManager, cookies, parallelthreadcount, cachedir, shouldapicache)
            SearchDispatcher.fetch_related_creators(repository, baseurl, proxyManager, cookies, parallelthreadcount, cachedir, shouldapicache)
            SearchDispatcher.fetch_user_videos(repository, proxyManager, parallelthreadcount, cachedir, shouldapicache=shouldapicache)

        return repository

    @classmethod
    def fetch_audience_distribution(cls, repository, baseurl, proxyManager, cookies, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request audience distribution for {len(repository)} authors')
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for authorid in repository.keys():
                dm = AudienceDistributionApiManager(baseurl, authorid, cookies, cachedir=cachedir, shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        dm.get, proxyManager=proxyManager
                    )
                )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    repository[authorid]['audience_dist'] = response['data']

    @classmethod
    def fetch_core_metrics(cls, repository, baseurl, proxyManager, cookies, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request core metrics for {len(repository)} authors')
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for authorid in repository.keys():
                dm = CoreMetricsApiManager(baseurl, authorid, cookies, cachedir=cachedir, shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        dm.get, proxyManager=proxyManager
                    )
                )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    repository[authorid]['core_metrics'] = response['data']

    @classmethod
    def fetch_trending_videos(cls, repository, baseurl, proxyManager, cookies, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request trending videos for {len(repository)} authors')
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for authorid in repository.keys():
                dm = TrendingVideosApiManager(baseurl, authorid, cookies, cachedir=cachedir, shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        dm.get, proxyManager=proxyManager
                    )
                )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    repository[authorid]['trending_videos'] = response['data']

    @classmethod
    def fetch_daily_fans(cls, repository, baseurl, proxyManager, cookies, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request daily fans for {len(repository)} authors')          
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for authorid in repository.keys():
                dm = DailyFansApiManager(baseurl, authorid, cookies, cachedir=cachedir, shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        dm.get, proxyManager=proxyManager
                    )
                )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    repository[authorid]['daily_fans'] = response['data']

    @classmethod
    def fetch_related_creators(cls, repository, baseurl, proxyManager, cookies, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request related creators for {len(repository)} authors')
        with concurrent.futures.ThreadPoolExecutor(parallelthreadcount) as executor:
            futures = []
            for authorid in repository.keys():
                dm = RelatedCreatorApimanager(baseurl, authorid, cookies, cachedir=cachedir, shouldapicache=shouldapicache)
                futures.append(
                    executor.submit(
                        dm.get, proxyManager=proxyManager
                    )
                )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    repository[authorid]['related_influencers'] = response['data']

    @classmethod
    def fetch_user_videos(cls, repository, proxyManager, parallelthreadcount=10, cachedir='__cache__', shouldapicache=None):
        print(f'Dispatching thread pool to request user video metadata for {len(repository)} authors')
        with Pool(parallelthreadcount) as pool:
            responses = pool.starmap(SearchDispatcher._exec, [(repository[id]['handle_name'], cachedir, shouldapicache) for id in repository.keys()])
            idx = 0
            for authorid in repository.keys():
                 repository[authorid]['video_metadata'] = responses[idx]
                 idx+=1

    @classmethod
    def _append_repo(cls, repository, response):
        for author in response['data']['authors']:
            id = author['id']
            repository[id] = author

    @classmethod
    def _exec(cls, author_handle, cachedir, shouldapicache):
        dm = TiktokScrapperManager(author_handle, cachedir=cachedir, shouldapicache=shouldapicache)
        return dm.get()
