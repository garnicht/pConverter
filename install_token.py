# %%
from sys import platform
import os

# %%
def ask_for_token(path):
    with open(path,"w") as file:
        token = input("Wie lautet dein token?:")
        content = f"weclapp_token = '{token}'"
        file.write(content)

# %%
def create_env(operating_sys):
    if operating_sys == "darwin":
        
        config_dir = os.path.expanduser("~/.config")
        env_file_path = os.path.join(config_dir, ".env")

        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
            ask_for_token(env_file_path)

        elif not os.path.exists(env_file_path):
            ask_for_token(env_file_path)

        ask_for_token(env_file_path)
        
    elif operating_sys == "win32":
        
        config_dir = os.path.expanduser("~\\AppData\\Local\\MyApp")
        env_file_path = os.path.join(config_dir, ".env")

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            ask_for_token(env_file_path)

        elif not os.path.exists(env_file_path):
            ask_for_token(env_file_path)
        
        ask_for_token(env_file_path)

    else:
        print("Betriebssystem wird nicht unterstützt")

# %%
create_env(platform)
input("Press enter to finish")


