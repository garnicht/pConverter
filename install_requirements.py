import subprocess
import platform

if platform.system() == "Darwin":
    subprocess.check_call(["python3", "-m", "pip", "install", "-r", "requirements.txt"])

elif platform.system() == "Windows":
    subprocess.check_call(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    input("Press enter to finish:")

else: 
    system = platform.system()
    print(f"This operating system {system} is not supported yet")