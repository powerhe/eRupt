from configparser import ConfigParser

class ConfigManager:
    _instance = None
    _file_name = None
    _config_object = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, file_name = "config.ini", config_object = ConfigParser()):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        if cls._instance._file_name != file_name:
            config_object.read(file_name)
            cls._instance._config_object = config_object
            cls._instance._file_name = file_name
            print("Reading config from file:", cls._instance._file_name)

        return cls._instance

    def get_config_set(self, config_set):
        return self._instance._config_object[config_set]

    def get_config(self, config_set, config_key):
        return self._instance._config_object[config_set][config_key]
        
if __name__ == "__main__":
    cm = ConfigManager.instance()
    print(cm.get_config('PROXY-CONFIG', 'username'))
    print(cm.get_config_set('PROXY-CONFIG'))