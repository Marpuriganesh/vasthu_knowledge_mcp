import yaml
def load_config(config_path: str):

    # Open and parse the YAML file
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config

config = load_config("src/curate_data/config.yml")