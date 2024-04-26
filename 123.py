import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import pandas as pd 
# import psycopg2
# import logging

today_date =  datetime.today().date()
curencies = ['MYR','KZT','KGS','UZS','AZN']
currencies_info_list = [] 
curr_responce = requests.get(str(os.getenv('CURRENCY_INFO_API')) + '2024/' + '1/3')
curr_responce_parsed = curr_responce.json()

for currency in curr_responce_parsed['rates']:
    if currency in(curencies):
            currencies_info_list.append({'report_date':today_date,'currency':currency,'rate':curr_responce_parsed['rates'][currency]})
exchange_rates = pd.DataFrame.from_dict(currencies_info_list)
print(exchange_rates)