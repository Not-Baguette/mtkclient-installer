import requests
import json
import os
import shutil
import platform
import sys
import re

def find_python_latest() -> str:
    """
    Finds latest python version in development
    """
    url = "https://www.python.org/doc/versions/"

    # Scrape latest release
    response = requests.get(url)

    # Use regular expressions to find the "In Development Versions"
    matches = re.findall(r'<a class="reference external" href="(https://docs.python.org/release/[\d.]+/)">Python ([\d.]+)</a>, documentation released on [\d\s\w]+', response.text)

    if matches:
        latest_version_url, latest_version_number = matches[0]
        print(f"Latest In Development Version: Python {latest_version_number}")
    else:
        print("Could not find the latest in development version.")
    return latest_version_number

def install_python(latest_version_number: str, arch_select: str) -> bool:
    """
    Downloads the latest version of python, this is a hacky solution but the best I can do for now
    """
    url_template = f"https://www.python.org/ftp/python/{latest_version_number}/python-{latest_version_number}"
    try:
        if arch_select == "64bit":
            url_template += "-amd64"
        elif arch_select == "32bit":
            pass
        else:
            raise NotImplementedError("Failed to detect architecture")
        
        url = url_template + ".exe"
        print(f"Downloading {url}...")

        # Download and install the app
        response = requests.get(url)
        with open("python_inst.exe", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        return False

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

def install_mediatek_drivers(asset_url: str, app_path: str) -> bool:
    """
    Installs the MTK Preloader Driver, static so no updates though
    """
    filename, driver_folder = "mtk_preloader_driver.zip", "mtk_preloader_driver"
    try:
        print("Getting assets...")
        response = requests.get(asset_url)
        print("Downloading drivers...")
        # Download the drivers
        with open(filename, "wb") as f:
            f.write(response.content)

        print("Unzipping & Installing drivers...")
        # Unzip the drivers & run the install drivers bat file
        shutil.unpack_archive(filename, driver_folder)
        abs_path =(os.path.join(app_path, driver_folder, 
                                "Mediatek Driver Auto Installer v1.1352"))  # this is static
        # cd to the dir first so the bat file can find required files
        os.system(f'cd "{abs_path}" && "Install Drivers.bat"')  

        return True
    except Exception as e:
        print(f"Failed to download Mediatek drivers: {e}")
        return False

def install_needed_packages(path_dict, arch: str, app_path: str) -> None:
    """
    Installs Winfsp, usbdk, and mediatek preloader drivers
    """
    winfsp_name, usbdk_name, git_name = "winfsp.msi", "usbdk.msi", "git_inst.exe"  # Dynamic naming
    # Install WinFSP
    if pull_latest_release(path_dict["winfsp"], winfsp_name):
        print("Please follow the Installation wizard that has popped up on your screen")
        os.startfile(winfsp_name)
        input("Press any key to continue...")

    # Installs usbdk
    if pull_latest_release(path_dict["usbdk"], usbdk_name):
        os.startfile(usbdk_name)
        input("Press any key to continue...")

    # Install git
    if arch == "64bit":
        print("64-bit detected")
    elif arch == "32bit":
        print("32-bit detected")
    else:
        raise NotImplementedError("Failed to detect architecture")
    
    pull_latest_release(path_dict["git"], git_name, arch_select=arch)
    
    # Start git installer
    print("Please follow the Installation wizard that has popped up on your screen")
    os.system(f'"{app_path}\\{git_name}"')
    input("Press any key to continue...")

def install_mtkclient() -> bool:
    """
    Downloads the mtkclient from repo, don't use release version incase it is not up to date like v1.58
    """
    try:
        logs = os.popen("git clone https://github.com/bkerler/mtkclient && cd mtkclient && pip3 install -r requirements.txt")
        if "https://visualstudio.microsoft.com/visual-cpp-build-tools" in logs.read():
            print("Netifaces build error detected")
            print("Please install Visual Studio Code from https://visualstudio.microsoft.com/visual-cpp-build-tools and then download 'Desktop Development with C++'")
    except OSError:
        return False
    # Open mtkclient, avoid using popen here.
    os.system("cd mtkclient && start . && start cmd.exe")
    return True
    

def main():
    # Dictionary of paths and URLs needed
    path_dict = {"winfsp": "https://api.github.com/repos/winfsp/winfsp/releases/latest",
                 "usbdk": "https://api.github.com/repos/daynix/UsbDk/releases/latest",
                 "git": "https://api.github.com/repos/git-for-windows/git/releases/latest",
                 "mtk preloader driver": "https://androiddatahost.com/wp-content/uploads/Mediatek_Driver_Auto_Installer_v1.1352.zip"}
    arch = platform.architecture()[0]

    # Intro text
    text_tup = ("Mtkclient Installer", 
             "By: Baguette - https://github.com/Not-Baguette/mtkclient-installer/", 
             "Version: 1.4-Chicago", 
             "Copyright: © Baguette 2024. All rights reserved.")

    print("-" * os.get_terminal_size().columns)
    for item in text_tup:
        print(item.center(os.get_terminal_size().columns))
    print("-" * os.get_terminal_size().columns)

    # Check if the script is running as an executable or as a python script, and changes the path accordingly
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
        # if it's run as an executable, install python
        if install_python(find_python_latest(), arch): # the function should return true if the installation was successful
            print("Please add Python as PATH on the installation wizard (near the bottom of the wizard)")
            os.system("python_inst.exe")
            input("Press any key to continue...")
    else:
        app_path = os.path.dirname(__file__)

    # Install WinFSP, usbdk, git and mediatek preloader drivers
    print("Winfsp/Usbdk/Git Installation successful.") if install_needed_packages(
        path_dict, arch, app_path) else print("Winfsp/Usbdk/Git Installation failed.")
    
    print("Mtk Preloader Driver Installation successful.") if install_mediatek_drivers(
        path_dict["mtk preloader driver"], app_path) else print("Mtk Preloader Driver Installation failed.") # Install MTK Preloader Driver
    
    # Download and unzip mtkclient
    print("Mtkclient Installation successful.") if install_mtkclient() else print("Mtkclient Installation failed.")


    print("-" * os.get_terminal_size().columns)
    print("Installation successful, you may close this window now.".center(os.get_terminal_size().columns))
    input("-" * os.get_terminal_size().columns) # use input here to avoid closing the window on .exe version

if __name__ == "__main__":
    main()
