import os, json

class ApiCacheManager:
    @classmethod
    def write_cache(cls, dir, key, data):
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(dir + "/" + key + '.json', 'w', encoding="utf8") as f:
            f.write(data)

    @classmethod
    def get_cache(cls, dir, key):
        try:
            with open(dir + "/" + key + '.json', 'r', encoding="utf8") as f:
                res = f.read()
                return None if len(res) == 0 else json.loads(res)
        except:
            return None