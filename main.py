import requests
import json
import os
import shutil
import platform
import sys

def pull_latest_release(url: str, filename: str, arch_select: str = "") -> bool:
    """
    Pulls the latest release from github, used for winfsp, usbdk, and git installation
    """
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        print(f"Latest release: {data['tag_name']}")

        if arch_select == "":
            asset_url = data["assets"][0]["browser_download_url"]  # Gets the latest release asset URL
        else:
            if arch_select == "64bit":
                filter = "-64-bit.exe"
            
            elif arch_select == "32bit":
                filter = "-32-bit.exe"

            # Find it depending on the architecture
            asset_url = data["assets"]
            for asset in asset_url:
                if asset["name"].endswith(filter):
                    asset_url = asset["browser_download_url"]
                    break
            
        print(f"Asset URL found: {asset_url}")
        
        response = requests.get(asset_url)
        print(f"Downloading {filename}...")

        # Download and install the app
        with open(filename, "wb") as f:
            f.write(response.content)

        return True
    except Exception as e:
        raise NotImplementedError(f"Failed to download {filename}: {e}")

def install_mediatek_drivers(asset_url: str, filename: str, app_path: str) -> bool:
    """
    Installs the MTK Preloader Driver
    """
    try:
        print("Getting assets...")
        response = requests.get(asset_url)
        print("Downloading drivers...")
        # Download the drivers
        with open(filename, "wb") as f:
            f.write(response.content)

        print("Unzipping & Installing drivers...")
        # Unzip the drivers & run the install drivers bat file
        shutil.unpack_archive("mtk_preloader_driver.zip", "mtk_preloader_driver")
        abs_path =(os.path.join(app_path, "mtk_preloader_driver", 
                                "Mediatek Driver Auto Installer v1.1352"))
        # cd to the dir first so the bat file can find required files
        os.system(f'cd "{abs_path}" && "Install Drivers.bat"')  

        return True
    except Exception as e:
        print(f"Failed to download Mediatek drivers: {e}")
        return False

def install_needed_packages(path_dict) -> None:
    """
    Installs Winfsp, usbdk, and mediatek preloader drivers
    """
    # Install WinFSP
    if pull_latest_release(path_dict["winfsp.msi"], "winfsp.msi"):
        print("Please follow the Installation wizard that has popped up on your screen")
        os.startfile("winfsp.msi")
        input("Press any key to continue...")

    # Installs usbdk
    if pull_latest_release(path_dict["usbdk.msi"], "usbdk.msi"):
        os.startfile("usbdk.msi")
        input("Press any key to continue...")

def download_mtkclient() -> bool:
    """
    Downloads the mtkclient from repo, don't use release version incase it is not up to date like v1.58
    """
    os.system(f"git clone https://github.com/bkerler/mtkclient && cd mtkclient && pip3 install -r requirements.txt")

def main():
    # Dictionary of paths and URLs needed
    path_dict = {"winfsp.msi": "https://api.github.com/repos/winfsp/winfsp/releases/latest",
                 "usbdk.msi": "https://api.github.com/repos/daynix/UsbDk/releases/latest",
                 "git": "https://api.github.com/repos/git-for-windows/git/releases/latest",
                 "mtk_preloader_driver.zip": "https://androiddatahost.com/wp-content/uploads/Mediatek_Driver_Auto_Installer_v1.1352.zip"}
    
    # Check if the script is running as an executable or as a python script, and changes the path accordingly
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(__file__)


    "Installation successful." if install_needed_packages(path_dict) else "Installation failed." # Installs WinFSP, usbdk
    "Installation successful." if install_mediatek_drivers(path_dict["mtk_preloader_driver.zip"], "mtk_preloader_driver.zip", app_path) else "Installation failed." # Install MTK Preloader Driver
    
    # Install git
    arch = platform.architecture()[0]
    if arch == "64bit":
        print("64-bit detected")
    elif arch == "32bit":
        print("32-bit detected")
    else:
        raise NotImplementedError("Failed to detect architecture")
    
    pull_latest_release("https://api.github.com/repos/git-for-windows/git/releases/latest", "git_inst.exe", arch_select=arch)
    
    # Start git installer
    print("Please follow the Installation wizard that has popped up on your screen")
    os.system(f'"{app_path}\\git_inst.exe"')
    input("Press any key to continue...")
    
    # Download and unzip mtkclient
    try:
        logs = os.popen("git clone https://github.com/bkerler/mtkclient && cd mtkclient && pip3 install -r requirements.txt")
        if "https://visualstudio.microsoft.com/visual-cpp-build-tools" in logs.read():
            print("Netifaces build error detected")
            print("Please install Visual Studio Code from https://visualstudio.microsoft.com/visual-cpp-build-tools and then download 'Desktop Development with C++'")
    except OSError:
        pass
    # Open mtkclient, avoid using popen here.
    os.system("cd mtkclient && start . && start cmd.exe")

    print("-" * os.get_terminal_size().columns)
    print("Installation successful, you may close this window now.".center(os.get_terminal_size().columns))
    input("-" * os.get_terminal_size().columns) # use input here to avoid closing the window on .exe version

if __name__ == "__main__":
    text_list = ["Mtkclient Installer", "By: Baguette", "Version: 1.2"]
    print("-" * os.get_terminal_size().columns)
    for i in text_list:
        print(i.center(os.get_terminal_size().columns))
    print("-" * os.get_terminal_size().columns)

    main()
