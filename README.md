# please read readme file before test

### by default to run a file you need to enter docker-container with "docker-compose exec currency_exchange bash"
### after it you need to start the file with "python main.py"

### if no cli arguments are passed the default values are set to: 
#### latest(today) for date
#### usd for converted currency
#### kzt for currency to which u want to convert

### if you want to run it with different currencies/dates you need to specify the cli arguments as shown below
### sample run command "python main.py -f eur -t kgs -d 2024-03-05"

### It is not  stated in the taskfile to establish airflow instance so i just wrote a DAG

#### UTC is default timezone for airflow so i assumed it is used this way in project and used it as default in currency_exchange_dag.py
### it can be changed with default_timezone = 'smth' if u demand it

### free api i used only has data from 2024-03-02 to now on, so consider it when testing

#### code in main.py could be done a little bit faster without pandas df, with just dict and using cursor, but because the amount of the data is not so big pandas df is more convenient option (this commentary also appears in main.py)