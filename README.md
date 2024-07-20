# mtkclient-installer

![image](https://github.com/user-attachments/assets/0038bba5-4f5e-449a-9a07-acf41c4abdc7)

I made this to simplify tech support work I've been doing on XDA discord server in case I ever become inactive there. This code for the most part will be *self-updating* as it _searches for latest releases_ rather being stuck on a specific version.
### Only for Windows because I can't test on mac/linux

## Installation
### Via .exe installer (Recommended if you really don't know how to even install a driver)
- Click on the latest release on the right side panel
  
![image](https://github.com/user-attachments/assets/8e0b3d99-8850-4a09-b2aa-aa1b4167e14d)
- Click `mtkclient_installer.exe` to download it

![image](https://github.com/user-attachments/assets/b48af167-1a88-46f2-8778-c11fba0c32e7)
- Drag it on somewhere you want to install mtkclient on

![image](https://github.com/user-attachments/assets/b27614fb-4ad4-4e02-a72d-72a4c20805b0)
- Run the application by double-clicking it
- Follow the script instructions

### Via Python (Recommended if you already know basic file comprehension)
- Download [python](https://www.python.org/)
- Open python installation wizard, click Add as PATH on the bottom
- Open `main.py` script

![image](https://github.com/user-attachments/assets/541b04c3-0535-460b-9e6b-44b63036c0b8)
- Download it

![image](https://github.com/user-attachments/assets/ecb86a9f-af4c-45fa-8f44-ad5756cf0f71)
- Move `main.py` on your downloads folder to another folder you want to install mtkclient on
- Run `main.py` via opening a command prompt on the same folder (right-click, open in terminal for win 11 users) and then running `python main.py` (Or probably just run it by double clicking the python file)
- Follow the instructions given

## What will this install
- Python (Latest, 64/32 bit)
- winfsp (Latest)
- usbdk (Latest)
- git (Latest, 64/32 bit)
- Mediatek drivers (Static)
- mtkclient (Latest)

Once you've installed all these, it will automatically open a command prompt on mtkclient folder so you can just run the command be done with it.

## Todo for v1.4
- [ ] Remove naming the files directly and put it on a variable instead
- [ ] Probably get rid of `path_dict`
- [ ] ??? I am not sure tbh, This app should be self-sufficient since it will keep taking the latest build possible.

## Credits
- [bkerler](https://github.com/bkerler/) for mtkclient
- [git](https://github.com/git/), bane of my existence
- [mtkandroid](https://androidmtk.com/category/download) for being a great place to find mediatek stuff
- [winfsp](https://winfsp.dev/rel/)
- [usbdk](https://github.com/daynix/UsbDk/releases)
