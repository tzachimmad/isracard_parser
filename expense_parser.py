# -*- coding: utf-8 -*-
import csv
from bs4 import BeautifulSoup, SoupStrainer 

#filenames
isracard_fn = '/home/redbend/Downloads/sheta.xls'
key_database_fn = 'fixed.csv'
categories_db = 'businesses.csv'

#define vars
CASH_ENTRY = "משיכת מזומנים"

#dictionaries
expenses_dic = {}
categorized_expenss = {}
unlisted_entities = {}

def print_to_csv(output_file,key,value,new_line):
    output_file.write(key)
    output_file.write(",")
    output_file.write(str(value))
    if new_line:
        output_file.write("\n")

def insert_to_dic(key_var, sum_float, cash_reduct):
    tmp = expenses_dic.get(key_var, 0)
    expenses_dic[key_var]= sum_float + tmp
    if cash_reduct == CASH_ENTRY: #here reduct fixed expenses from cash entrys
        tmp = expenses_dic.get(cash_reduct, 0)
        expenses_dic[CASH_ENTRY]= tmp - sum_float

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

#parse isracard xls in html format
def parse_xls_html(path):
    htmlfile = open(path)
    xls_soup = BeautifulSoup(htmlfile)
    for item in xls_soup.findAll("tr"):
        if "NIS" in str(item):
            blocks = str(item).split('<td')
            if "grey" in blocks[0]:
                break
            if "><" not in blocks[1]:
                k = str(blocks[2]).find("<")
                key_var = blocks[2][1:k].replace("&#39;", "")
                key_var = key_var.replace("&quot;", "")
                sum_float =  float(blocks[4].split("</")[1][12:])
                insert_to_dic(key_var, sum_float, "")
    htmlfile.close

#function, loads sheet expenses to expenses database dictionary
def parse_expenses (path):
    f = open(path, 'rb')
    reader = csv.reader(f)
    for row in reader:
        insert_to_dic(row[0],float(row[1]),row[2])
    f.close()

##parse fixed bills
parse_expenses(key_database_fn)

##parse isracard bills
parse_xls_html(isracard_fn)

##set categories sums, unlisted sums
f = open(categories_db, 'rb')
reader = csv.reader(f)
uncategorized = set()
sum = 0
for key in expenses_dic:
    sum+=expenses_dic[key]
    cat = "unlisted category"
    f.seek(0)
    for row in reader:
        if key in row:
            cat = row[0]
            break
    tmp = categorized_expenss.get(cat, 0)
    categorized_expenss[cat] = tmp + expenses_dic[key]
    if cat == "unlisted category":
        uncategorized.add(key)
f.close()

##print categorized items
output_file = open("output.csv", 'w')
print_to_csv(output_file,"Financial Analysis","",True)
sum=0
for key in categorized_expenss:
    sum+=categorized_expenss[key]
    print key, categorized_expenss[key]
    print_to_csv(output_file,key,categorized_expenss[key],True)
print "סכום",sum
print_to_csv(output_file,"Sum",sum,True)
print_to_csv(output_file,"","",True)

##print items not categorized
if (len(uncategorized)>0):
    print "\nFollowing items not categorized"
    print_to_csv(output_file,"Following items not categorized","",True)
    for key in uncategorized:
        print key
        print_to_csv(output_file,key,"",True)
    print_to_csv(output_file,"","",True)

##print business Establishments:
print "\nTop Business Establishments:"
print_to_csv(output_file,"Top Business Establishments","",True)
pairs = sorted(expenses_dic.items(), key=lambda x: x[1])
for tuple in reversed(pairs):
    print tuple[0],":",tuple[1]
    print_to_csv(output_file,tuple[0],tuple[1],True)

output_file.close()
