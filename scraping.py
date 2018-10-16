from bs4 import BeautifulSoup
import requests
import datetime
from dateutil.parser import parse
from time import strptime, strftime
from database import createscheduledbconnection

def convertmonth(month):
    ''' function to convert month from string to integer '''
    try:
        ans = strptime(month,'%b.').tm_mon
    except:
        ans = strptime(month,'%b').tm_mon
    return ans
def scrape_last_episode(url):
    ''' function to scrape and get data from seasons schedule page of a tv series on imdb '''
    rs = requests.get(url)
    soups = BeautifulSoup(rs.text, "html.parser")
    dates = soups.find_all("div", {"class": "airdate"})# scrape all airdates from imdb
    dates = [d.string.strip() for d in dates]
    idate=[]
    for date in dates:
        if date=='':
            idate.append([0,0,0])
            continue
        date = date.split(' ')
        if len(date)==3:
            idate.append([int(date[0]),date[1],int(date[2])])
        elif len(date)==2:
            idate.append([0,date[0],int(date[1])])
        elif len(date)==1:
            idate.append([0,0,int(date[0])])
        else:
            idate.append([0,0,0])

    for date in idate:
        if date[1]!=0:
            date[1] = convertmonth(date[1])

    curdate=[datetime.date.today().day,datetime.date.today().month,datetime.date.today().year]
    ans=[]
    flag = False
    returnflag = False
    for date in idate: # check if a date is greater then current date
        if date[2]>curdate[2]:
            returnflag = True
            ans = date
            break
        elif date[1]>curdate[1] and date[2]>=curdate[2]:
            returnflag = True
            ans = date
            break
        elif date[0]>curdate[0] and date[2]>=curdate[2] and date[1]>=curdate[1]:
            returnflag = True
            ans = date
            break
        elif date[0]==0 and date[1]==0 and date[2]==curdate[2]:
            returnflag = True
            ans = date
            break
        flag=True
    ans = [str(i) for i in ans]

    if flag:
        sol = 'Next episode airs on'
        code = 1
    else:
        sol = 'The next season begins'
        code = 2

    if ans==[]:

        date = 'info not available'
        code = 3
    elif ans[0]=='0' and ans[1]=='0':
        date = parse(' '.join(ans[2:])).strftime('%Y')
    elif ans[0]=='0':
        date = parse(' '.join(ans[1:])).strftime('%b %Y')
    else:
        date = parse(' '.join(ans)).strftime('%d %b %Y')



    return returnflag,sol,date,code



def find_release_date(series, update,href):
    ''' function to check if a series is over and get data of next episode by scraping seasons in descending order '''
    urla = "http://www.imdb.com"+href
    rtv = requests.get(urla)
    souptv = BeautifulSoup(rtv.text, "html.parser")
    tagend = souptv.find("a", {"title": "See more release dates"})
    data = tagend.string.strip()
    mycursor, mydb = createscheduledbconnection()
    if data[-3]!='–': # check if a given series is over or has seasons/episode left
        sol = 'The show has finished streaming all its episodes.'
        code = 0
        date = ''
        sql = "INSERT INTO tvdata (title, detail, ddate, code) VALUES (%s, %s, %s, %s)"
        val = (series, sol, date, code)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        tagtv = souptv.find("div", {"class": "seasons-and-year-nav"})
        tagtv = tagtv.find_all("a")
        urls = "http://www.imdb.com"+str(tagtv[0]['href'])
        flag = True
        i = 0
        sol = 'Next expisode/season airs on'
        date = 'No info available'
        code = 3
        while flag: # recursion to check if current season has release dates greater then present date
            urls = "http://www.imdb.com"+str(tagtv[i]['href'])
            flag,so,dat,cod = scrape_last_episode(urls)
            if flag:
                sol,date,code = so,dat,cod
            i = i+1
        sql = "INSERT INTO tvdata (title, detail, ddate, code) VALUES (%s, %s, %s, %s)"
        val = (series, sol, date, code)
        if update:
            sql = "UPDATE tvdata SET detail = %s, ddate = %s, code = %s WHERE title = %s"
            val = (sol, date, code, series)
        mycursor.execute(sql, val)
        mydb.commit()

def checkdb(name):
    ''' this function checks the tvdata table in imdb database, if the database contains a particular schedule it will return that or it will search for the schedule by calling a different function '''
    name = name.strip().replace(" ","%20")
    url="http://www.imdb.com/find?q="+str(name)+"&s=tt&ttype=tv&ref_=fn_tv"
    r = requests.get(url) # get name of series as it is on imdb
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        tag = soup.find("td", {"class": "result_text"})
        series = str(tag.a.string)+str(tag.contents[2])
        href = tag.a["href"]
    except:
        return name.replace("%20"," "),'!'
    mycursor, mydb = createscheduledbconnection()
    sql = "SELECT * FROM tvdata where title = %s;" # check db if it contains data about a particular series
    val = (series,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    update = False
    if myresult and myresult[0][3]==0:
        return name.replace("%20"," "),series
    elif myresult and myresult[0][3]==1:
        date = parse(myresult[0][2])
        if date.date()<datetime.date.today():
            update =True
        else:
            return name.replace("%20"," "),series
    elif myresult and myresult[0][3]==2:
        if int(myresult[0][2])<=datetime.date.today().year:
            update = True
        else:
            return name.replace("%20"," "),series
    elif myresult and myresult[0][3]==3:
        update = True

    find_release_date(series,update,href)
    return name.replace("%20"," "),series # retuen name input by user and name of series in database for mailing purpose
