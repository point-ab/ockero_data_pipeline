# install.py
import os
import sys
import subprocess
import platform

def create_venv():
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

def activate_venv():
    system = platform.system()
    if system == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        return f"call {activate_script}"
    else:  # macOS/Linux
        activate_script = os.path.join("venv", "bin", "activate")
        return f"source {activate_script}"

def install_requirements():
    print("Installing project in editable mode...")
    activate_cmd = activate_venv()
    if platform.system() == "Windows":
        subprocess.run(f"{activate_cmd} && pip install -e .", shell=True)
    else:
        subprocess.run(f"{activate_cmd} && pip install -e .", shell=True, executable="/bin/bash")

def create_data_folder():
    print("Creating 'data' folder...")
    if not os.path.exists("data"):
        os.makedirs("data")

def create_env_file():
    print("Creating '.env' file...")
    with open(".env", "w") as f:
        f.write("SS12000_SECRET=xxxx\n")

def main():
    create_venv()
    install_requirements()
    create_data_folder()
    create_env_file()
    print("Installation complete!")

if __name__ == "__main__":
    main()
