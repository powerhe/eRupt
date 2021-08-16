import csv, os, sys, datetime

class CsvOutputManager:
    def __init__(self, directory, repository, category, maxnum=sys.maxsize) -> None:
        self._dir = directory
        self._repo = repository
        self._category = category
        self._maxnum = int(maxnum)
        if self._maxnum == 0:
            self._maxnum = int(sys.maxsize)

    def _write_CSV(self, filename, labels, data):
        data.sort(key=lambda r: r[0])
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
        with open(self._dir + "/" + filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(labels)
            writer.writerows(data)

    def write_age(self):
        filename = 'age.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Percentage,Age'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for age in author['audience_dist']['age']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(age['value']*100)
                    row.append(age['property'])
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_gender(self):
        filename = 'gender.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Percentage,Gender'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for gender in author['audience_dist']['gender']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(gender['value']*100)
                    row.append(gender['property'])
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_tiktok_category(self):
        filename = 'tiktok_category.csv'
        labels = 'Influencer ID,Category,Tiktok Category'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for tiktok_category in author['topics']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append(tiktok_category)
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_followers_trending(self):
        filename = 'follower_trending.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Followers Counts,Time'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for stat in author['daily_fans']['daily_statistics']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(stat['cnt'])
                    row.append(stat['date'])
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_follower_region_states(self, topstatepick=sys.maxsize):
        topstatepick = int(topstatepick)
        filename = 'follower_region_states.csv'
        labels = 'Influencer ID,Category,Tiktok Category,States,Percentage'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                regions = author['audience_dist']['state']
                regions.sort(key=lambda r: -r['value'])
                for region in regions[:topstatepick]:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(region['property'])
                    row.append(region['value']*100)
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_follower_region_countries(self, topcountrypick=sys.maxsize):
        topcountrypick = int(topcountrypick)
        filename = 'follower_region_countries.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Country,Percentage'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                regions = author['audience_dist']['region']
                regions.sort(key=lambda r: -r['value'])
                for region in regions[:topcountrypick]:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(region['property'])
                    row.append(region['value']*100)
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_related_influencers(self):
        filename = 'related_influencers.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Related Influencer ID,Follower Count, Average View Count'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for rauthor in author['related_influencers']['authors']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(rauthor['handle_name'])
                    row.append(rauthor['reach'])
                    row.append(rauthor['avg_views'])
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_core_metrics(self):
        filename = 'influencer_samples.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Average Views,Likes,Comments Counts,Shares,Region,Follower Counts,Score'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                metric = author['core_metrics']['recent_30_items']['avg']
                row = []
                row.append(author['handle_name'])
                row.append(self._category)
                row.append('|'.join(author['topics']))
                row.append(metric['views'])
                row.append(metric['hearts'])
                row.append(metric['comment'])
                row.append(metric['shares'])
                row.append(author['region'])
                row.append(author['reach'])
                row.append(metric['engagement'])
                data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_trending_videos(self):
        filename = 'trending_videos.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Video ID,Video Desc,View Counts,Temporal'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for video in author['trending_videos']['hottest']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(video['item_id'])
                    row.append(video['title'])
                    row.append(video['views'])
                    row.append(datetime.datetime.fromtimestamp(video['create_time']).strftime('%Y/%m/%d'))
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_video_metadata(self):
        filename = 'videos_information.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Video ID,Likes,Comments,Shares,Video Desc,View Counts,Temporal,URL'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for video in author['video_metadata']:
                    row = []
                    row.append(author['handle_name'])
                    row.append(self._category)
                    row.append('|'.join(author['topics']))
                    row.append(video['id'])
                    row.append(video['diggCount'])
                    row.append(video['commentCount'])
                    row.append(video['shareCount'])
                    row.append(video['text'])
                    row.append(video['playCount'])
                    row.append(datetime.datetime.fromtimestamp(video['createTime']).strftime('%Y/%m/%d'))
                    row.append(video['videoUrl'])
                    data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)

    def write_hashtags(self):
        filename = 'hashtags.csv'
        labels = 'Influencer ID,Category,Tiktok Category,Hashtags,View Counts'.split(',')
        data = []
        cnt = 0
        for author in self._repo.values():
            cnt+=1
            if cnt > self._maxnum:
                break
            try:
                for video in author['video_metadata']:
                    for hashtag in video['hashtags']:
                        row = []
                        row.append(author['handle_name'])
                        row.append(self._category)
                        row.append('|'.join(author['topics']))
                        row.append(hashtag['name'])
                        row.append(video['playCount'])
                        data.append(row)
            except:
                pass
        self._write_CSV(filename, labels, data)
    