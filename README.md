# isracard_parser
Parses expenses from downloaded isracard monthly xls.
Produces a report in csv file and outputs neccessary information to screen.
All output is in Hebrew.

expense_parser.py is the code file

buisinesses.csv is the database of establishments setup into categories

fixed.csv are fixed expenses not included in the mastercard output. here u
have the ability of writing an expense as a cash expense and thus this expense
will be deducted out of cash withdrawals.
if an entry is listed as "משיכת מזומנים" then it is subjected to being a cash withdrawal expense,
otherwise it is a regular expense
