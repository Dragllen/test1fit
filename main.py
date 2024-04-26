import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import pandas as pd 
import psycopg2
import logging
import sqlalchemy

logger = logging.getLogger(__name__)

def get_currencies_rate(today_date,curencies):
    currencies_info_list = [] 
    curr_responce = requests.get(os.getenv('CURRENCY_INFO_API'))
    curr_responce_parsed = curr_responce.json()

    for currency in curr_responce_parsed['rates']:
        if currency in(curencies):
                currencies_info_list.append({'report_date':today_date,'currency':currency,'rate':curr_responce_parsed['rates'][currency]})
    exchange_rates = pd.DataFrame.from_dict(currencies_info_list)
    return exchange_rates

def database_upload(currencies_df):

    conn_postgre = sqlalchemy.create_engine(
    f'postgresql+psycopg2'
    f'://{os.getenv("POSTGRE_USER")}'
    f':{os.getenv("POSTGRE_PASS")}'
    f'@{os.getenv("POSTGRE_HOST")}'
    f':5432'
    f'/{os.getenv("POSTGRE_DB")}'
)

    with conn_postgre.begin() as con:
        currencies_df.to_sql('daily_exchange_rate_usd', schema = 'public', con=con, if_exists='replace', index=False)  

def main():
    load_dotenv()
    today_date =  datetime.today().date()
    curencies = ['MYR','KZT','KGS','UZS','AZN']
    exchange_rates = get_currencies_rate(today_date,curencies)

    logger.warning('trying to connect to db')
    try:
        database_upload(exchange_rates)    
    except:
        logger.warning('cant connect to db')
    else:
        logger.warning('connected  to db')
if __name__ == "__main__":
    main()