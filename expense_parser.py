# -*- coding: utf-8 -*-
from expense_class import *
import csv
import xlrd
import datetime
from datetime import date
from isracard_update import *
from os import remove

#download directory
download_dir = '/home/redbend/Downloads/'

#filenames
isracard_fn = 'sheta.xls'
key_database_fn = 'fixed.csv'
categories_db = 'businesses.csv'
credinitials_fn = '/home/redbend/Desktop/training/python scripts/credinitials.csv'
chrome_driver_path = '/home/redbend/Desktop/training/Hackathon/chromedriver'

#define vars
CASH_ENTRY = "משיכת מזומנים"
UNLISTED_CATEGORY = "unlisted category"
IGNORE_ISRACARD_ENTRY = "סך חיוב בש\"ח:"

#dictionaries
expense_list = []
establishment_dic = {}
category_dic = {}

def print_to_csv(output_file,key,value,new_line):
    key = key.replace(",","")
    key = key.replace("\'","")
    key = key.replace("\"","")
    output_file.write(key)
    output_file.write(",")
    output_file.write(str(value))
    if new_line:
        output_file.write("\n")

#Create Expense and Relative Establishment and put in appropriate set
def add_expense(date_made, estab_name, amount, cash):
    if estab_name in establishment_dic:
        estab = establishment_dic[estab_name]
    else:
        estab = Establishment(estab_name)
        establishment_dic[estab_name] =  estab
    expense_input = Expense(date_made, estab, amount, cash)
    estab.add_expense(expense_input)
    expense_list.append(expense_input)
    if cash:
        if CASH_ENTRY not in establishment_dic:
            establishment_dic[CASH_ENTRY] = Establishment(CASH_ENTRY)
        tmp = establishment_dic.get(CASH_ENTRY)
        tmp.set_amount(tmp.get_amount() - int(amount))

#parse isracard xls in html format
def parse_xls_html(path):
    book = xlrd.open_workbook(filename=path, encoding_override="cp1252")
    first_sheet = book.sheet_by_index(0)
    row = 6
    keep_parsing = True
    while keep_parsing:
        establishment = first_sheet.cell(row,1).value
        if (establishment == IGNORE_ISRACARD_ENTRY):
            row += 1
            if first_sheet.cell(row,1).value == xlrd.empty_cell.value:
                keep_parsing = False
            continue
        amount = first_sheet.cell(row,3).value
        date_made = first_sheet.cell(row,0).value
        add_expense(date_made, establishment, float(amount[1:]), False)
        row +=1

#function, loads sheet expenses to expenses database dictionary
def parse_expenses (path):
  ##  date_made = expense_list[0].get_date()
    date_made = datetime.date.today()
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        add_expense(date_made, str(row[0]), str(row[1]), str(row[2]) == CASH_ENTRY)
    f.close()

##set categories sums, unlisted sums
def set_categories():
    f = open(categories_db, 'rb')
    reader = csv.reader(f)
    uncategorized = Category(UNLISTED_CATEGORY)
    category_dic[UNLISTED_CATEGORY] = uncategorized
    for key in establishment_dic:
        estab = establishment_dic[key]
        cat = UNLISTED_CATEGORY
        f.seek(0)
        for row in reader:
            if key in row:
                cat = row[0]
                break
        if cat not in category_dic:
            category_dic[cat] = Category(cat)
        curr_category = category_dic.get(cat)
        curr_category.add_establishment(estab)
        estab.set_category(curr_category)
    f.close()

##clean download directory
clean_directory(download_dir)


##download relative isracard sheet
if sys.argv[1].find("download_sheet")>=0:
    a,b,c = read_credinitials(credinitials_fn)
    downloadLatestSheet(a,b,c,chrome_driver_path)

##set correct isracard sheet file name
    isracard_fn = retrieve_isracard_sheet(download_dir)
else:
    isracard_fn = sys.argv[1]

##parse fixed bills
parse_expenses(key_database_fn)

##parse isracard bills
parse_xls_html(isracard_fn)

##set categories sums, unlisted sums
set_categories()

##print categorized items
output_file = open("output.csv", 'w')
print_to_csv(output_file,"Financial Analysis","",True)
sum=0
for key in category_dic:
    cat_input=category_dic[key]
    sum += cat_input.get_amount()
    if cat_input.get_amount() > 0:
        print key, cat_input.get_amount()
        print_to_csv(output_file,key,cat_input.get_amount(),True)
print "סכום",sum
print_to_csv(output_file,"Sum",sum,True)
print_to_csv(output_file,"","",True)

##print items not categorized
uncategorized = category_dic[UNLISTED_CATEGORY]
if (uncategorized.get_amount() > 0):
    print "\nFollowing items not categorized"
    print_to_csv(output_file,"Following items not categorized","",True)
    for estab in uncategorized.get_establishments():
        print estab.get_name()
        print_to_csv(output_file,estab.get_name(),"",True)
    print_to_csv(output_file,"","",True)

##print business Establishments:
print "\nTop Business Establishments:"
print_to_csv(output_file,"Top Business Establishments","",True)
pairs = sorted(establishment_dic.items(), key=lambda x: x[1].get_amount())
for tuple in reversed(pairs):
    estab = tuple[1]
    print estab.get_name(),":",estab.get_amount()
    print_to_csv(output_file, estab.get_name(), estab.get_amount(), True)

output_file.close()
remove(isracard_fn)