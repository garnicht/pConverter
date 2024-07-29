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
def get_env_path():
    if platform == "darwin":
        config_dir = os.path.expanduser("~/.config")
        env_file_path = os.path.join(config_dir, ".env")

    elif platform == "win32":
        myapp_dir = os.path.expanduser("~\\AppData\\Local\\MyApp")
        env_file_path = os.path.join(myapp_dir, ".env")

    return env_file_path

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

        else:
            ask_for_token(env_file_path)
        
    elif operating_sys == "win32":
        
        myapp_dir = os.path.expanduser("~\\AppData\\Local\\MyApp")
        env_file_path = os.path.join(myapp_dir, ".env")

        if not os.path.exists(myapp_dir):
            os.makedirs(myapp_dir)
            ask_for_token(env_file_path)

        elif not os.path.exists(env_file_path):
            ask_for_token(env_file_path)
        
        else:
            ask_for_token(env_file_path)

    else:
        print("Betriebssystem wird nicht unterstützt")

# %%
if __name__ == "__main__":
    create_env(platform)
    input("Press enter to finish")