from database import createscheduledbconnection, createuserdbconnection
from scraping import checkdb
from mail import send_email
from multiprocessing import Pool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def main():
    print('SCHEDULE ALERTER!!\nEnter your email address and the list of tv series.\nWe use imdb to gather data so to get accurate data enter tv deries name in the format NAME (Year of release).')
    usersno = int(input('Enter no of users:-'))
    # connecting to user database and save each input in the database
    usercursor, userdb = createuserdbconnection()
    for i in range(usersno):
        mail = input('Email address:-')
        name = input("Enter name of tv series:-")
        sql = "INSERT INTO userinput (email, tvseries) VALUES (%s, %s)"
        val = (mail, name)
        usercursor.execute(sql, val)
        userdb.commit()

    # getting the last userno from database and looping over them and sending mail
    sql = "SELECT * FROM userinput;"
    usercursor.execute(sql)
    userresult = usercursor.fetchall()
    userresult = userresult[-usersno:]
    for user in userresult:
        name = user[1].split(',')
        print('Fetching data from imdb')
        # multithreading to make process faster
        with Pool(5) as p:
            ans = p.map(checkdb, name)
        print('Preparing a mail')
        sub = "Schedule of upcoming tv episodes"
        text = "Here are the details you requested\n\n"
        html = "Here are the details you requested<br><br>"
        mycursor, mydb = createscheduledbconnection()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sub
        msg['From'] = config.EMAIL
        msg['To'] = user[0]
        # prepare a bady for mail by iterating over user input
        for a in ans:
            if a[1]!='!':
                sql = "SELECT * FROM tvdata where title = %s;"
                val = (a[1],)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                text = text + "Tv Series Name: {}  IMDB Name- {}\nStatus: {} {}\n\n".format(a[0],myresult[0][0],myresult[0][1],myresult[0][2])
                html = html + "Tv Series Name: <b>{}</b>   <small><i>IMDB Name</i>- {}</small><br>Status: {} {}<br><br>".format(a[0],myresult[0][0],myresult[0][1],myresult[0][2])
            else:

                text = text + "Tv Series Name: {}\nStatus: {} \n\n".format(a[0],'No such tv series exists')
                html = html + "Tv Series Name: <b>{}</b><br>Status: {} <br><br>".format(a[0],'No such tv series exists')
        part1 = MIMEText(text, 'text')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        send_email(sub,msg,user[0])
if __name__=='__main__':
    main()
