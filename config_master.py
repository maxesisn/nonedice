import os
import json
import fuckit


class Config(object):
    fd = os.path.dirname(__file__)

    # 用replace很难看，以后一定修
    with open(os.path.join(fd, "config/personalization.json"), "r") as f:
        personalization = json.load(f)

    def __init__(self) -> None:
        super().__init__()

    def get(self, config_name, group_id, user_id=None):
        group_id = str(group_id)
        if user_id is not None:
            user_id = str(user_id)
        self.loader()

        config: dict = getattr(self, config_name)
        try:
            if group_id not in getattr(self, config_name):
                getattr(self, config_name)[group_id] = {}
            if user_id is not None and user_id not in getattr(self, config_name)[group_id]:
                getattr(self, config_name)[group_id][user_id] = {}
            if user_id is not None:
                return config[group_id][user_id]
            else:
                return config[group_id]
        except KeyError:
            print("KeyError exception passed")

    def set(self, config_name, content, group_id, user_id=None):
        group_id = str(group_id)
        if user_id is not None:
            user_id = str(user_id)
        self.loader()

        try:
            if group_id not in getattr(self, config_name):
                getattr(self, config_name)[group_id] = {}
            if user_id is not None and user_id not in getattr(self, config_name)[group_id]:
                getattr(self, config_name)[group_id][user_id] = {}
            if user_id is not None:
                getattr(self, config_name)[group_id][user_id] = content
            else:
                getattr(self, config_name)[group_id] = content
            self.saver()
        except KeyError:
            print("KeyError exception passed")
            

    def clr(self, config_name, group_id, user_id=None):
        group_id = str(group_id)
        if user_id is not None:
            user_id = str(user_id)
        self.loader()

        try:
            config = getattr(self, config_name)
            if user_id is not None:
                del config[group_id][user_id]
            else:
                del config[group_id]
            self.saver()
        except KeyError:
            print("KeyError exception passed")
            return None


class GeneralConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.dice = {}
        self.player = {}
        self.ob = {}
        self.loader()

    @fuckit
    def loader(self):
        with open(os.path.join(self.fd, "config/dice.json"), "r") as f:
            self.dice = json.load(f)
        with open(os.path.join(self.fd, "config/player.json"), "r") as f:
            self.player = json.load(f)
        with open(os.path.join(self.fd, "config/ob.json"), "r") as f:
            self.ob = json.load(f)

    def saver(self):
        with open(os.path.join(self.fd, "config/dice.json"), "w") as f:
            json.dump(self.dice, f, indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/player.json"), "w") as f:
            json.dump(self.player, f, indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/ob.json"), "w") as f:
            json.dump(self.ob, f, indent=4, ensure_ascii=False)


class COCConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.template = {}
        self.profile = {}
        self.loader()

    @fuckit
    def loader(self):
        with open(os.path.join(self.fd, "config/COC/template.json"), "r") as f:
            self.template = json.load(f)
        with open(os.path.join(self.fd, "config/COC/profile.json"), "r") as f:
            self.profile = json.load(f)

    def saver(self):
        with open(os.path.join(self.fd, "config/COC/template.json"), "w") as f:
            json.dump(self.template, f,
                      indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/COC/profile.json"), "w") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)
