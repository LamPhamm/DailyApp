import mysql.connector

db=mysql.connector.connect(
    host='localhost',
    user='Lam',
    passwd='waterBell$73',
    database='dailyAppData'
)
myCursor=db.cursor()

#myCursor.execute('CREATE TABLE DailyEntry (Date VARCHAR(10) PRIMARY KEY, Highlight VARCHAR(1000), statusHighlight boolean DEFAULT FALSE, \
                 #highlightImageLink VARCHAR(100),Todo TEXT(60000))')