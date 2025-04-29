import getpass
import json
import os.path

def load_key(keyname: str) -> object:
    file_name = "keys.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            Key = json.load(file)
        if keyname in Key and Key[keyname]:
            return Key[keyname]
        else:
            keyval = getpass.getpass("配置文件中需要的配置信息，请输入: ").strip()
            Key[keyname] = keyval
            with open(file_name, "w") as file:
                json.dump(Key, file, indent=4)
            return keyval
    else:
        keyval = getpass.getpass("配置文件中需要的配置信息，请输入: ").strip()
        Key = { keyname: keyval }
        with open(file_name, "w") as file:
            json.dump(Key, file, indent=4)
        return keyval