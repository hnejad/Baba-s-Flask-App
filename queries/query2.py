import mysql.connector
import datetime
import calendar

now = datetime.datetime.now()

def query():
    mydb = mysql.connector.connect(
      host="reporting.waterguru-prod.com",
      user="wgtableau",
      password="UIENnehe272lswHWENW62290HEOPNWYNM",
      database="prod_reporting"
    )

    mycursor = mydb.cursor()

    mycursor.execute('''
    select podid, remoteMoistRecCount, remoteMoistLevMin, lastLowMoistValTime, remoteTempAve, lastCxnTime 
from (select podId as podid, count(remoteMoistLev1) as remoteMoistRecCount, min(remoteMoistLev1) as remoteMoistLevMin , max(time) as lastLowMoistValTime, avg(remoteTempFahr) as remoteTempAve from pod_debug where  remoteMoistLev1  < 65535 group by podid) as a
left join (select podId as ay, lastCxnTime from pod ) as b 
on podid = ay
group by podid
order by podid
    ''')

    myresult = mycursor.fetchall()
    parsedData = []
    for row in myresult:
        r = []
        for cell in row:
            if(isinstance(cell,float)):
                c = str(cell)[0:5]
                r.append(c)
            elif(isinstance(cell,datetime.datetime)):
                c = cell.strftime("%Y/%m/%d")
                
                #str(cell.day) + " " + str(calendar.month_name[cell.month]) + ", " + str(cell.year)
                r.append(c)
            else:
                r.append(cell)
        parsedData.append(r)

    return parsedData

def getQuery2():
    description = "This is the table description"
    headers = ['PodId', 'data points', 'Lowest Moisture level', 'Last low reading', 'Ave Temperature', 'Last connection']
    data = query()
    q = {'data':data,'headers':headers, 'description':description}
    return q