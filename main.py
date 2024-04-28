import getopt, sys, os
from dotenv import load_dotenv
import requests
from datetime import datetime
import pandas as pd 
import psycopg2
import logging
import sqlalchemy

logger = logging.getLogger(__name__)

def get_currencies_rate(date, currency_for_rate, currency_converted):

    curr_responce = requests.get(f'{os.getenv("CURRENCY_INFO_API")}{date}/{os.getenv("apiVersion")}/{os.getenv("endpoint")}/{currency_for_rate}.json'.format()) 

    if date == 'latest':
        date = datetime.today().date()
    data_to_upload = {'ds':date,'currency_from':currency_for_rate,'currency_to':currency_converted,'rate':curr_responce.json()[currency_for_rate][currency_converted]}
    
    # this could be done a little bit faster without pandas df, with just dict and using cursor,
    # but because the amount of the data is not so big pandas df is more convenient option (this commentary also appears in readme.md)

    exchange_rates = pd.DataFrame.from_dict([data_to_upload])

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
        currencies_df.to_sql('daily_exchange_rate_usd', schema = 'public', con=con, if_exists='append', index=False)  

def main():
    load_dotenv()
    try:
        currency_for_rate = 'usd'
        currency_converted = 'kzt'
        date = 'latest'
        for currentArgument in range(1, len(sys.argv), 2):

            if sys.argv[currentArgument] in ("-d", "--date"):
                date = sys.argv[currentArgument+1]
                
            elif sys.argv[currentArgument] in ("-f", "--from"):
                currency_for_rate = sys.argv[currentArgument+1]
                
            elif sys.argv[currentArgument] in ("-t", "--to"):
                currency_converted = sys.argv[currentArgument+1]

    except getopt.error as err:
        print (str(err)) 

    exchange_rates = get_currencies_rate(date, currency_for_rate, currency_converted)

    logger.warning('trying to connect to db')
    try:
        database_upload(exchange_rates)    
    except Exception as exs:
        logger.warning('cant connect to db')
        logger.warning("Exception while connection to db %s" ,str(exs), exc_info=True)
    else:
        logger.warning('connected  to db')

if __name__ == "__main__":
    main()