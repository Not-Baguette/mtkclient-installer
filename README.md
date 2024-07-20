![image](https://github.com/user-attachments/assets/f4e094b0-f019-4bf8-9f22-6de0901590ee)# mtkclient-installer

![image](https://github.com/user-attachments/assets/0038bba5-4f5e-449a-9a07-acf41c4abdc7)

I made this to simplify tech support work I've been doing on XDA discord server in case I ever become inactive there. This code for the most part will be self-updating as it searches for latest releases.
### Only for Windows because I can't test on mac/linux

## Installation
### Via .exe installer (Currently still needs manual python installation, will be fixed soon)
![image](https://github.com/user-attachments/assets/0a65bd5a-f9dd-4117-94f8-03bae5c1dc76)
- Click `main.exe` to download it
![image](https://github.com/user-attachments/assets/65a28916-127a-498a-817a-38b39f36dfc9)
- Drag it on somewhere you want to install mtkclient on
![image](https://github.com/user-attachments/assets/b27614fb-4ad4-4e02-a72d-72a4c20805b0)
- Double click the file on the folder you want install mtkclient on
- Download [python](https://www.python.org/)
- Open python installation wizard, click Add as PATH on the bottom
- Click on the latest release like shown below

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
- winfsp
- usbdk
- git (64/32 bit)
- Mediatek drivers
- mtkclient
Once you've installed all these, it will automatically open a command prompt on mtkclient folder so you can just run the command be done with it.

## Todo
## For .exe release (Personal Notes)
Bugs on exe version to deal with:
- [X] Git and the drivers not being installed due to using relative path I guess, Make this work with pyinstaller by putting objective paths So it wont run on `\AppData\Local\Temp\`
![image](https://github.com/user-attachments/assets/293d191f-5c2f-47fd-8619-35ce0c9f56b2)
- [X] mtkclient installation failed completely, maybe can't git clone?
- [X] Disable automatically closing by changing the last line to be `input()`
- [ ] Installs latest python for you on the .exe one
## For code quality
- [X] Make it so it uses a variable rather than splitting it into two functions at line 19-33
- [X] Same with line 109 and 112 probably
- [ ] Either decouple git into it's own function or put everything on `main()` function 

## Credits
- [bkerler](https://github.com/bkerler/) for mtkclient
- [git](https://github.com/git/), bane of my existence
- [mtkandroid](https://androidmtk.com/category/download) for being a great place to find mediatek stuff
- [winfsp](https://winfsp.dev/rel/)
- [usbdk](https://github.com/daynix/UsbDk/releases)
