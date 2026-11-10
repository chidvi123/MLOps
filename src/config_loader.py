import yaml

class ConfigLoader:

    def __init__(self,config_path="configs/config.yaml"):
        with open(config_path,"r") as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config