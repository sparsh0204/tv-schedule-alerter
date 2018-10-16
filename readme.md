# TV Schedule Alerter

Just run the script and enter email and list of tv series and you will get the next airing date of tv series through mail.

## Getting Started

### Prerequisites
Install these packages
* Python3
* BeautifulSoup ==4.6.3
* mysql-connector==2.1.6
* requests==2.19.1
* mysql

You can install the individually by using ``` $ pip install PACKAGE-NAME``` or

You can install them at once by running the command
```
 $ pip install -r requirements.txt
```

### Setup
You must have mysql installed on your pc.

First clone the reprositery and navigete inside the directory using ```cd <Directory-name>```make a virtuall environment by using the command
```
 $ virtualenv -p /usr/bin/python3 venv
```

Then start the virtual environment by 
```
 $ source venv/bin/activate
```

Install the dependencies given in prerequisites

Open the config.py and enter your details
```
EMAIL='YOUR_EMAIL'
PASSWORD='YOUR_EMAIL_PASSWORD'
DATABASE_HOST='MYSQL_DATABASE_HOST'
DATABASE_USER='MYSQL_DATABASE_USER'
DATABASE_PASSWORD='MYSQL_DATABASE_PASSWORD'
```

Run the main script by using command 
```
 $ python3 main.py
```

## Usage
Just enter the emailid and list of tv series and the script will scrape imdb to get the latest dates and then mail the results to you.
 
