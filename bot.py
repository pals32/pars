from tkinter import *
import json
import time
from bs4 import BeautifulSoup
import requests
import fake_useragent
import os

root = Tk()
root.geometry('300x400')
ua = fake_useragent.UserAgent()
def get_name():
    l3['text']= ent.get()
def get_salary():
    l4['text']= ent.get()

def owsalT():
    l6['text'] = "True"

def owsalF():
    l6['text'] = "False"

def get_vac():
    text = l3.cget('text')
    salar = l4.cget('text')
    owsal = l6.cget('text')

 # try:
 #     int(salar)
 # except:
 #     print("restart")
 #     os.execv(sys.executable, ['py'] + sys.argv)

    if os.path.exists(f"./db/{text}_{salar}.json") == True:
        with open(f"db/{text}_{salar}.json") as file:
             file.read()
    else:
        if salar != '0':
            def get_links(text):
                data = requests.get(
                    url=f"https://hh.ru/search/vacancy?text={text}&ored_clusters=true&salary={salar}&only_with_salary={owsal}&area=1&page=0",
                    headers={"user-agent": ua.random}
                )
                if data.status_code != 200:
                     return
                soup = BeautifulSoup(data.content, 'lxml')
                try:
                    page_count = int(
                        soup.find('div', {"class": "pager"}).find_all("span", recursive=False)[-1].find('a').text)
                except:
                    return
                for page in range(page_count):
                    try:
                        data = requests.get(
                            url=f"https://hh.ru/search/vacancy?text={text}&ored_clusters=true&area=1&salary={salar}&only_with_salary={owsal}&page={page}",
                            headers={"user-agent": ua.random}
                        )
                        if data.status_code != 200:
                            continue
                        soup = BeautifulSoup(data.content, "lxml")
                        for a in soup.find("span", {"class": "serp-item__title-link-wrapper"}).find_all('a', href=True):
                            yield f'{a['href']}'

                    except Exception as e:
                        print(f"{e}")
                    time.sleep(1)

            def get_vacancy(link):
                data = requests.get(
                    url=link,
                    headers={"user-agent": ua.random}
                )
                if data.status_code != 200:
                    return
                soup = BeautifulSoup(data.content, "lxml")
                try:
                    name = soup.find("h1", {"class": 'bloko-header-section-1'}).text
                    try:
                        salary = soup.find('span', {"data-qa": "vacancy-salary-compensation-type-net"}).text.replace("\xa0", " ")
                    except:
                        salary = soup.find('span', {"data-qa": "vacancy-salary-compensation-type-gross"}).text.replace("\xa0", " ")
                except:
                    name = ''
                vacancy = {
                    "name": name,
                    "salary": salary,
                    "url": link
                }
                return vacancy

            if __name__ == "__main__":
                list = []
                for a in get_links(text):
                    #time.sleep(1)
                    print(get_vacancy(a))
                    list.append(get_vacancy(a))

                with open(f"./db/{text}.json", "w", encoding="utf-8") as file:
                    json.dump(list, file, indent=4, ensure_ascii=False)

        else:
            def get_links(text):
                data = requests.get(
                    url=f"https://hh.ru/search/vacancy?text={text}&ored_clusters=true&only_with_salary={owsal}&area=1&page=0",
                    headers={"user-agent": ua.random}
                )
                if data.status_code != 200:
                    return
                soup = BeautifulSoup(data.content, 'lxml')
                try:
                    page_count = int(
                        soup.find('div', {"class": "pager"}).find_all("span", recursive=False)[-1].find('a').text)
                except:
                    return
                for page in range(page_count):
                    try:
                        data = requests.get(
                            url=f"https://hh.ru/search/vacancy?text={text}&ored_clusters=true&only_with_salary={owsal}&area=1&page={page}",
                            headers={"user-agent": ua.random}
                        )
                        if data.status_code != 200:
                            continue
                        soup = BeautifulSoup(data.content, "lxml")
                        for a in soup.find("span", {"class": "serp-item__title-link-wrapper"}).find_all('a', href=True):
                            yield f'{a['href']}'

                    except Exception as e:
                        print(f"{e}")
     #                  time.sleep(1)

            def get_vacancy(link):
                data = requests.get(
                    url=link,
                    headers={"user-agent": ua.random}
                )
                if data.status_code != 200:
                    return
                soup = BeautifulSoup(data.content, "lxml")
                try:
                    name = soup.find("h1", {"class": 'bloko-header-section-1'}).text
                    try:
                        salary = soup.find('span', {"data-qa": "vacancy-salary-compensation-type-net"}).text.replace(
                            "\xa0", " ")
                        salary = soup.find('span', {"data-qa": "vacancy-salary-compensation-type-gross"}).text.replace(
                            "\xa0", " ")
                    except:
                        salary = "Уровень дохода не указан"
                except:
                    name = ''
                vacancy = {
                    "name": name,
                    "salary": salary,
                    "url": link
                }
                return vacancy

            if __name__ == "__main__":
                list = []
                for a in get_links(text):
                   #time.sleep(0.3)
                   print(get_vacancy(a))
                   list.append(get_vacancy(a))
                with open(f"./db/{text}_{salar}.json", "w", encoding="utf-8") as file:
                   json.dump(list, file, indent=4, ensure_ascii=False)
    l5['text']='done'

ent = Entry(root)
l1=Label(root, text="name")
l2=Label(root, text="salary")
l3=Label(root, bg='black', fg='white')
l4=Label(root, bg='black', fg='white')
l5=Label(root, bg='black', fg='white')
l6=Label(root)
btn1 = Button(root, text='Name_vacancy', command=get_name)
btn2 = Button(root, text='Salary', command=get_salary)
btn3 = Button(root, text='Start', command=get_vac)

var_chk = IntVar()
rd1 = Radiobutton(root, text="salary", variable=var_chk, value=1, command=owsalT)
rd2 = Radiobutton(root, text="no salary", variable=var_chk, value=2, command=owsalF)

l1.grid(row=1)
l2.grid(row=2)
l3.grid(row=3)
l4.grid(row=4)
l5.grid(row=5)
ent.grid(row=1, column=1)
rd1.grid(row=2, column=1, sticky=W)
rd2.grid(row=2, column=1, sticky=E)
btn1.grid(row=1, column=3)
btn2.grid(row=1, column=4)
btn3.grid(row=2, column=3)

text = l3.cget('text')
salar = l4.cget('text')
owsal = l6.cget('text')




root.mainloop()











