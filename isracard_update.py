#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir, remove
import sys
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

reload(sys)
sys.setdefaultencoding('utf-8')

def downloadLatestSheet(user_id, card_info, pass_word,chrome_driver_path):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/home/redbend/Desktop/training/python scripts/whatsapp_poll-master") #Path to your chrome profile
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
    driver.set_window_size(1024,768)
    driver.get('https://digital.isracard.co.il/personalarea/login/')
    driver.find_element(By.ID, 'otpLoginID').clear()
    driver.find_element(By.ID, 'otpLoginID').send_keys(user_id)
    driver.find_element_by_id("otpLoginLastDigits").clear()
    driver.find_element_by_id("otpLoginLastDigits").send_keys(card_info)
    driver.find_element_by_id("otpLoginPwd").clear()
    driver.find_element_by_id("otpLoginPwd").send_keys(pass_word)
    driver.find_element_by_xpath("(//button[@type='submit'])[1]").click()
    time.sleep(1)
    driver.get('https://digital.isracard.co.il/personalarea/transaction-list/');
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id=\"wholePageExport\"]/div[5]/div/div/div/div[1]/div[1]/ul/li[1]/img").click()
    time.sleep(5)
    driver.find_element_by_link_text(u"יציאה").click()
    driver.quit()

def read_credinitials(filename):
    f = open(filename, 'rb')
    csv_rows = csv.reader(f)
    user_id = next(csv_rows)[1]
    card_info  = next(csv_rows)[1]
    pass_word  = next(csv_rows)[1]
    f.close()
    return user_id, card_info, pass_word

def clean_directory(dir):
    for f in listdir(dir):
        if 'Export_' in f:
            try:
                remove(dir + f)
            except OSError:
                pass

def retrieve_isracard_sheet(dir):
    for f in listdir(dir):
        if 'Export_' in f:
            return dir + f
    return -1



