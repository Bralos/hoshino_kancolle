import requests
import urllib.request
import re
import bs4
from bs4 import BeautifulSoup

def get_ship_list():
    #returns a dictionary, containing the ship names and their link
    ship_list = {}
    #ship_name = []
    source=requests.get('http://w.kcwiki.moe:8080/wiki/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4')
    #来源：舰娘百科
    soup=bs4.BeautifulSoup(source.text,'lxml') #'lxml' processes the html
    for n in range(5): #priliminary test, only first 150 ships.
        name = soup.select("td")[n]('a')[0]["title"]
        if name != "未实装":
            herf = soup.select("td")[n]('a')[0]["href"]
            link = f"http://w.kcwiki.moe:8080{herf}"
            #ship_name.append(name)#can be replaced by ship_list.keys?
            ship_list.update([(name,link)])
        n += 1
    #ship_name = ship_list.keys()
    #print(ship_name)
    return ship_list

def text_extraction(soup):
    text = list(soup.stripped_strings)
    hc_text = []
    try:
        index = text.index("〇〇〇〇时报") #0000文本。
        #hc_mp3 = []
        for hours in range(24):
            cmb = text[index+1] + text[index+2] #合并中日文报时文本
            hc_text.append(cmb)
            #mp3_url =
            #hc_mp3
            index += 7 #到下一个时报的index
    except Exception as e:
        #print(e)
        print('无报时文本')
    return hc_text

def voice_extraction(soup):
    audio_list = soup.find_all('ul', attrs = {"class":"sm2-playlist-bd"})
    hc_url = []
    for ele in audio_list:
        if '0.mp3' in ele.a['data-filesrc']:
            # only select files with the form
            # ***0.mp3
            hc_url.append(ele.a['data-filesrc'])
    return hc_url

def download_file(url):
    file = requests.get(url)
    file_name = url[url.rindex('/')+1:]
    with open(file_name,'wb') as f:
        f.write(file.content)

def get_hour_res(ship_list,end=-1):
    #get the hour call text from the ship list. get all if end = -1.
    #will write a py file to record.
    #will download all the mp3 files

    ship_number = [] # a list of ships by their number.
                     # Will be used to name their hourcall and locate the voice file
    ship_text_dict = {}
    if end == -1:
        for name in ship_list.keys():
            url = ship_list.get(name) #link to the ship's page
            ship_ct = requests.get(url) # page content
            soup = bs4.BeautifulSoup(ship_ct.text,'lxml')

            hc_text = text_extraction(soup)
            if hc_text != []:
                voice_list = voice_extraction(soup)

                """
                This code block generates a file for each ship.

                start = voice_list[0].rindex('/')+1
                end = voice_list[0].rindex('-')

                f = open(f'{voice_list[0][start:end]}.py',"w",encoding="utf-8")
                # create a file, to write in the name and the voice lines.
                f.write(voice_list[0][start:end]+' \n')
                for ele in hc_text:
                    f.write(str(ele)+'\n')
                f.close()
                """
                #The following code block appends the text and name to two seperate
                #list for generating the config/hour_call.py file.
                start = voice_list[0].rindex('/')+1
                end = voice_list[0].rindex('-')
                number = str(voice_list[0][start:end])

                #ship_text_collective.append(hc_text)
                ship_text_dict.update([(str(number),hc_text)])
                ship_number.append(number)
                for ele in voice_list:
                    download_file(ele)
    f = open('hourcall_config.py','w',encoding = 'utf-8')
    f.write(f"HOUR_CALLS_ON = {str(ship_number)} \n\nHOUR_CALLS = {ship_text_dict}")
    f.close()

ship_list = get_ship_list()
get_hour_res(ship_list)
print('完成')
