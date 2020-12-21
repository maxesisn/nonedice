# 内存吞噬者 启动！
import os
try:
    import ujson as json
except:
    import json

class Config(object):

    def __init__(self, gid) -> None:
        super().__init__()
        self.path = os.path.join(os.path.dirname(__file__), "config")
        self.config_list = os.listdir(self.path)
        self.gid = str(gid)

    def load(self, sub_id) -> dict:
        sub_id=str(sub_id)

        if f"{self.gid}.json" not in self.config_list:
            self.group_config=dict()    
        else:
            with open(os.path.join(self.path,f"{self.gid}.json"), "r") as f:
                self.group_config=json.load(f)
        
        if sub_id not in self.group_config:
            self.group_config[sub_id]=dict()
        return self.group_config[sub_id]
        
    def save(self):
        with open(os.path.join(self.path,f"{self.gid}.json"), "w") as f:
            json.dump(self.group_config, f, indent=4, ensure_ascii=False)
