import os
import json
class Config():
    def __init__(self):
        pass
    def get_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt",'r')as f:
                config_data = f.read()
            return json.loads(config_data)
        else:
            return ""
    def set_config(self,data):
            with open("config.txt", 'w') as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))