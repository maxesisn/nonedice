import os
import json
import fuckit
from collections import defaultdict


class Config(object):
    fd = os.path.dirname(__file__)

    def __init__(self) -> None:
        super().__init__()

    def get(self,config_name):
        return getattr(self, config_name, None)

    def mod(self,config_name, content):
        setattr(self, config_name, content)

    def clr(self,config_name):
        delattr(self, config_name)


class GeneralConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.dice_config = defaultdict(lambda: defaultdict(dict))
        self.player_config = defaultdict(lambda: defaultdict(dict))
        self.ob_config = {}
        self.loader()

    @fuckit
    def loader(self):
        with open(os.path.join(self.fd, "config/dice.json"), "r") as f:
            self.dice_config = json.load(f)
        with open(os.path.join(self.fd, "config/player.json"), "r") as f:
            self.player_config = json.load(f)
        with open(os.path.join(self.fd, "config/ob.json"), "r") as f:
            self.ob_config = json.load(f)
        print("dice general config loaded")

    def saver(self):
        with open(os.path.join(self.fd, "config/dice.json"), "w") as f:
            json.dump(self.dice_config, f, indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/player.json"), "w") as f:
            json.dump(self.player_config, f, indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/ob.json"), "w") as f:
            json.dump(self.ob_config, f, indent=4, ensure_ascii=False)
        print("dice general config saved")


class COCConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.coc_template_config = defaultdict(lambda: defaultdict(dict))
        self.coc_profile_config = defaultdict(lambda: defaultdict(dict))
        self.loader()

    @fuckit
    def loader(self):
        with open(os.path.join(self.fd, "config/COC/template.json"), "r") as f:
            self.coc_template_config = json.load(f)
        with open(os.path.join(self.fd, "config/COC/profile.json"), "r") as f:
            self.coc_profile_config = json.load(f)
        print("dice COC config loaded")

    def saver(self):
        with open(os.path.join(self.fd, "config/COC/template.json"), "w") as f:
            json.dump(self.coc_template_config, f,
                      indent=4, ensure_ascii=False)
        with open(os.path.join(self.fd, "config/COC/profile.json"), "w") as f:
            json.dump(self.coc_profile_config, f, indent=4, ensure_ascii=False)
        print("dice COC config saved")
