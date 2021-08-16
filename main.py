from requests.auth import HTTPBasicAuth
from src.apimanager import AudienceDistributionApiManager
from src.signinmanager import SigninManager
from src.proxymanager import ProxyManager, ProxyPolicy
from src.configmanager import ConfigManager
from src.dispatcher import SearchDispatcher
from src.csvoutputmanager import CsvOutputManager
from src.countrymap import countrymap

def main():
    proxyConfig = ConfigManager.instance().get_config_set('PROXY-CONFIG')
    targetConfig = ConfigManager.instance().get_config_set('TARGET-CONFIG')
    localConfig = ConfigManager.instance().get_config_set('LOCAL-CONFIG')

    proxyManager = ProxyManager(proxyConfig['proxylisturl'],    \
                                proxyConfig['username'],        \
                                proxyConfig['password'],        \
                                ProxyPolicy.ROUND_ROBIN)
    proxyManager.refresh_proxy_list()

    isauthcacheenabled = 'y' in localConfig['authcacheenabled'].lower()
    signinManager = SigninManager(localConfig['chromepath'],                    \
                                 targetConfig['domain'],                        \
                                 cachedir=localConfig['cachedir'],              \
                                 authcache=isauthcacheenabled)                  \
    
    cookies = signinManager.get_cookies()

    topics = [topic.strip() for topic in targetConfig['searchtopics'].split(',')]
    country = countrymap[targetConfig['country']] if targetConfig['country'] != "" else None
    for topic in topics:
        print ('Fetching data for category:' + topic)
        isapicacheenabled = 'y' in localConfig['apicacheenabled'].lower()
        repository = SearchDispatcher.dispatch('https://' + targetConfig['domain'],                             \
                                                proxyManager,                                                   \
                                                topic,                                                          \
                                                cookies,                                                        \
                                                country=country,                                                \
                                                maxnum=localConfig['maxnumberofinfluencers'],                   \
                                                parallelthreadcount=int(localConfig['parallelthreadcount']),    \
                                                cachedir=localConfig['cachedir'],                               \
                                                shouldapicache=isapicacheenabled)
        
        csvManager = CsvOutputManager(localConfig['outputdir'] + "/" + topic, repository, topic, maxnum=localConfig['maxnumberofinfluencers'])
        csvManager.write_age()
        csvManager.write_gender()
        csvManager.write_tiktok_category()
        csvManager.write_follower_region_countries(topcountrypick=3)
        csvManager.write_follower_region_states(topstatepick=3)
        csvManager.write_followers_trending()
        csvManager.write_related_influencers()
        csvManager.write_core_metrics()
        csvManager.write_trending_videos()
        csvManager.write_video_metadata()
        csvManager.write_hashtags()
    exit(0)

if __name__ == "__main__":
    main()