from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import requests
import os
import datetime

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont


# 메뉴얼
def manual():
    now = datetime.datetime.now().strftime('%y%m%d_%H%M')
    messagebox.showinfo("manual", "1. URL을 입력해주세요.\n"
                                  "2. 원하는 위치에 다운받기를 원하면 폴더 선택을 눌러 경로를 설정해주세요.\n"
                                  " # 경로 미설정시 실행 파일 위치 기준으로 생성됩니다 #\n"
                                  "3. Start 버튼을 누르면 해당 폴더 위치에 "+now+" 폴더가 생성된 후 다운로드됩니다.\n")
# 디렉토리 설정
def select_Directory():

    selectDirectory = filedialog.askdirectory() + "/"
    entDirectory.delete(0,"end")
    entDirectory.insert(0,selectDirectory)
    print("logger - selectDirectory "+selectDirectory)

# 크롤링 & 이미지 다운
def crawling(url):
    try:
        saveDirectory = Entry.get(entDirectory)  # 파일 저장 위치
        now = datetime.datetime.now().strftime('%y%m%d_%H%M')
        # 경로 빈값일 때 현재위치 설정
        if saveDirectory == "":
            print('logger - Directory : ' +os.getcwd())
            saveDirectory = os.getcwd() + "/"
        elif saveDirectory[-1] != "/":  # 마지막 문자열 / 체크
            saveDirectory += "/"

        #selenium
        webDriver_options = webdriver.ChromeOptions()
        webDriver_options.add_argument('headless')

        driver = webdriver.Chrome('./util/chromedriver',options=webDriver_options)
        driver.get(url)

        # req = requests.get(url)
        # soup = BeautifulSoup(req.content, "html.parser")
        # imgList = soup.findAll('img')

        images = driver.find_elements_by_css_selector("img")

        result = []
        print(images)
        for img in images:
            if 'gif' in img.get_attribute('src'):
                continue
            if 'https://ssl' in img.get_attribute('src'):
                continue
            if 'https://map' in img.get_attribute('src'):
                continue
            result.append(img.get_attribute('src'))


        saveDirectory += now + "/"

        print("logger - 최종 saveDirectory 위치 확인: "+saveDirectory)
        try:
            if not os.path.exists(saveDirectory):
                os.makedirs(saveDirectory)
        except OSError:
            print('Error: Can\'t create a directory. ' + saveDirectory)

        i = 1
        for img in result:
            # print(img)
            urllib.request.urlretrieve(img, saveDirectory + str(i) + ".jpg")
            # urlretrieve(img, saveDirectory  + str(i) + '.jpg')
            i +=1

        # i = 1
        # for img in imgList:
        #     # .gif 파일 스킵
        #     if '.gif' in img['src']:
        #         continue
        #     print(img)
        #     # print(img['src'])
        #     if 'data-lay-src' in img:
        #         print('11')
        #     img = re.sub("_blur", "0", img['src'])
        #     # img = urllib.parse.quote_plus(img, safe='://')

            # if '.PNG' in img:
            #     urllib.request.urlretrieve(urllib.parse.quote_plus(img, safe='://'), saveDirectory + str(i) + ".png")
            # elif '.JPEG' in img:
            #     urllib.request.urlretrieve(urllib.parse.quote_plus(img, safe='://'), saveDirectory + str(i) + ".jpeg")
            # elif '.jpg' in img:
            #     urllib.request.urlretrieve(urllib.parse.quote_plus(img, safe='://'), saveDirectory + str(i) + ".jpg")

            # urllib.request.urlretrieve(img, saveDirectory + str(i) + ".jpg")
            # i += 1
        if os.path.exists(saveDirectory):
            messagebox.showinfo("Complete", "다운이 완료되었습니다 :)")
        else:
            messagebox.showinfo("Alert", "이미지 다운을 실패하였습니다 :(")
    except Exception as e:
        print(e)
        # messagebox.showinfo("Alert", "이미지 다운을 실패하였습니다 :(\n"+str(e))
        pass

def start_button():
    crawlingUrl = Entry.get(ent)
    print("logger - start_button url " + crawlingUrl)
    if crawlingUrl is not "":
        crawling(crawlingUrl)
    else:
        messagebox.showinfo("Alert", "값을 입력해주세요.")

def clear_button():
    ent.delete("0", "end")

if __name__ == '__main__':
    # tkinter Setting
    app = Tk()
    app.title("GUI Crawler v1.0")  # 창 타이틀
    app.geometry("300x200+800+400")  # 창 크기
    font = tkFont.Font(family="Consolas", size=14, weight="bold")

    currentDirectory = os.getcwd() # 현재위치
    print("logger - currentDirectory "+currentDirectory)

    # 메뉴바
    menubar = Menu(app)
    menu1 = Menu(menubar,tearoff=0)
    menu1.add_command(label="Manual",command=manual)
    menu1.add_command(label="test2")
    menu1.add_command(label="test3")
    menubar.add_cascade(label="File", menu=menu1)

    # URL 설정
    label = Label(app, text="URL을 입력하세요.", font=font)
    label.pack(pady=20)

    # URL 입력창
    ent = Entry(app, width=40)
    ent.pack()

    # URL 입력창
    entDirectory = Entry(app, width=40)
    entDirectory.insert(0,currentDirectory)
    entDirectory.pack()

    # 버튼
    selectFolderBtn = Button(app, text="폴더 선택", width=10, command=select_Directory)
    selectFolderBtn.pack(padx=10, pady=10)

    startBtn = Button(app, text="Start", width=10, command=start_button)
    startBtn.pack(side='left', padx=30, pady=10)

    clearBtn = Button(app, text="Clear", width=10, command=clear_button)
    clearBtn.pack(side='right', padx=30, pady=10)

    app.config(menu=menubar)
    app.mainloop()