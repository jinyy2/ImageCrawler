from bs4 import BeautifulSoup
import urllib.request
import requests
import os
import datetime

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont


#
def manual():
    messagebox.showinfo("manual", "1. URL을 입력해주세요.\n"
                                  "2. 원하는 위치에 다운받기를 원하면 Folder를 눌러 경로를 설정해주세요.\n"
                                  " # 경로 미설정시 실행 파일 위치 기준으로 생성됩니다 #\n"
                                  "3. Start 버튼을 누르면 해당 폴더 위치에 "+now+" 폴더가 생성된 후 다운로드됩니다.\n")
def select_folder():
    global saveDir
    saveDir = filedialog.askdirectory() + "/" + now + "/"
    print("1"+saveDir)
    pass

#크롤링 & 이미지 다운
def crawling(url):
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        imgList = soup.findAll('img')
        print("2"+saveDir)

        try:
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
        except OSError:
            print('Error: Creating directory. ' + saveDir)

        i = 1
        for img in imgList:
            img = re.sub("_blur", "0", img['src'])
            urllib.request.urlretrieve(img, saveDir + str(i) + ".jpg")
            i += 1
        if os.path.exists(saveDir):
            messagebox.showinfo("Complete", "다운이 완료되었습니다 :)")
        else:
            messagebox.showinfo("Alert", "이미지 다운을 실패하였습니다 :(")
    except Exception:
        print('Parse Error!')

def start_button():
    url = Entry.get(ent)
    print(url)
    if url is not "":
        crawling(url)
    else:
        messagebox.showinfo("Alert", "값을 입력해주세요.")

def clear_button():
    ent.delete("0", "end")

if __name__ == '__main__':
    # tkinter Setting
    app = Tk()
    app.title("GUI Crawler v1.0")  # 창 타이틀
    app.geometry("300x200+800+400")  # 창 크기
    font = tkFont.Font(family="Consolas", size=16, weight="bold")

    menubar = Menu(app)
    menu1 = Menu(menubar,tearoff=0)
    menu1.add_command(label="Manual",command=manual)
    menu1.add_command(label="test2")
    menu1.add_command(label="test3")
    menubar.add_cascade(label="File", menu=menu1)
    label = Label(app, text="URL을 입력하세요.", font=font)
    label.pack(pady=30)

    # URL 입력창
    ent = Entry(app, width=30)
    ent.pack()

    now = datetime.datetime.now().strftime('%y%m%d_%H%M')
    saveDir = "C:/Images/" + now + "/"

    startBtn = Button(app, text="Folder", width=10, command=select_folder)
    startBtn.pack(padx=10, pady=10)

    startBtn = Button(app, text="Start", width=10, command=start_button)
    startBtn.pack(side='left', padx=30, pady=10)

    clearBtn = Button(app, text="Clear", width=10, command=clear_button)
    clearBtn.pack(side='right', padx=30, pady=10)

    app.config(menu=menubar)
    app.mainloop()