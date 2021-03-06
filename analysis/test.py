from bs4 import BeautifulSoup;
import csv;
import pandas as pd;
import time;
from selenium import webdriver;
import os;
from selenium.webdriver.common.keys import Keys

num=input("How many data file are there?\n");

def getImageLink(tags):
    links=[];
    for x in tags:
        for y in x:
            beam = y.attrs['data-bem']
            start = beam.find('{"url":"');
            start = start + 8
            end = beam.find('","fileSizeInBytes', start);
            links.append(beam[start:end]);
            break;
    return links;

def getTitle(tags):
    title=[];
    for x in tags:
        for y in x:
            beam = y.attrs['data-bem']
            start = beam.find('title":"');
            start = start + 8;
            end = beam.find('","hasTitle', start);
            title.append(beam[start:end]);
            break;
    return title;

def getDescription(tags):
    description=[];
    for x in tags:
        for y in x:
            for j in y.findAll('img'):
                description.append(j.attrs['alt']);
                break;
    return description;

def getAllFiles():
    files_list=[];
    for root, dirs, files in os.walk("data"):
        for filename in files:
            files_list.append(filename)
    return files_list;
print(getAllFiles());

def findWhetherCSVContains50Data(filename):
    split_filename=filename.split('.')
    file=pd.read_csv("data/"+filename);
    count=len(file.Title)
    if(count>=50):
        return True;
    else:
        return False;


filename=[];
filename=getAllFiles();
if(os.path.exists('data') and len(filename)!=0):
    filename=getAllFiles();
    for i,file in enumerate(filename):
        print(i,file)
        if(findWhetherCSVContains50Data(file)):
            pass;
        else:
            data_front=file.split('.')[0];
            encoded_url = 'https%3A%2F%2Fsolmolandra.000webhostapp.com%2Fdata%2F'+data_front+'.jpg';
            search_query = 'https://yandex.com/images/search?img_url=' + encoded_url + '&rpt=imagelike';
            driver = webdriver.Chrome("chromedriver.exe");
            driver.get(search_query);
            #driver.execute_script("window.scrollTo(0, 18950);")
            #print(page.__len__())
            elem=driver.find_element_by_tag_name("body");
            no_of_pagedown=20;
            while(no_of_pagedown):
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2);
                no_of_pagedown-=1;
            # page=requests.get(search_query);
            page = driver.execute_script('return document.documentElement.outerHTML')
            driver.close()
            tags = []
            if (True):
                soup = BeautifulSoup(page, "html5lib");
                count = 0;
                for j in range(1200):
                    val = soup.findAll("div", {
                        "class": "serp-item serp-item_type_search serp-item_group_search serp-item_pos_" + str(
                            j) + " serp-item_scale_yes justifier__item i-bem"})
                    if (val != []):
                        tags.append(val);
                        count += 1;
                        if (count >= 50):
                            break;

                dataframe_data = {
                    'Title': getTitle(tags),
                    'Description': getDescription(tags),
                    'Link': getImageLink(tags),
                }
                df = pd.DataFrame(dataframe_data);
                try:
                    os.makedirs('data');
                except FileExistsError:
                    pass;
                df.to_csv("data\\data" + str(i+1) + ".csv");
                print("Successfull");