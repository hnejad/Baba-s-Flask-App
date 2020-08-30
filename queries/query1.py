import mysql.connector
import datetime


def query():
    mydb = mysql.connector.connect(
      host="reporting.waterguru-prod.com",
      user="wgtableau",
      password="UIENnehe272lswHWENW62290HEOPNWYNM",
      database="prod_reporting"
    )

    mycursor = mydb.cursor()

    mycursor.execute('''
    select podCounts, Total_Pod, ifnull(Pod_Remote_Moisture,0), ifnull(Pod_Remote_Moisture,0) / Total_Pod * 100 as Perc
    from( 
      select count(pd) as Total_Pod ,
      CASE WHEN pd between 1 and 1599 THEN '00-Before EDVT'
        WHEN pd between 1600 and 1999 THEN '01-EDVT'
        WHEN pd between 2000 and 2999 THEN '02-PVT-1'
        WHEN pd between 3000 and 3121 THEN '02-PVT-2.1'
        WHEN pd between 3122 and 3249 THEN '03-PVT-2.2.1'
        WHEN pd between 3250 and 3999 then '04-PVT-2.2.2'
        WHEN pd between 4000 and 5999 then '05-MP1'
        WHEN pd between 6000 and 6449 then '06-MP2.1'
        WHEN pd between 6450 and 6999 then '07-MP2.2'
        WHEN pd between 7000 and 7854 then '08-MP3'
        WHEN pd between 7855 and 8999 then '09-MP4'
        WHEN pd between 9000 and 11000 then '10-MP5'
            WHEN pd between 100000 and 11000000 then '11-TREAT'
        else 'ELSE'
      END as podCounts 
      from (select podId as pd from pod_event_count where podId > 0 group by podId) as a
      group by podCounts
      ) as root
    left join (
      select count(pd) as Pod_Remote_Moisture,
      CASE WHEN pd between 1 and 1599 THEN '00-Before EDVT'
        WHEN pd between 1600 and 1999 THEN '01-EDVT'
        WHEN pd between 2000 and 2999 THEN '02-PVT-1'
        WHEN pd between 3000 and 3121 THEN '02-PVT-2.1'
        WHEN pd between 3122 and 3249 THEN '03-PVT-2.2.1'
        WHEN pd between 3250 and 3999 then '04-PVT-2.2.2'
        WHEN pd between 4000 and 5999 then '05-MP1'
        WHEN pd between 6000 and 6449 then '06-MP2.1'
        WHEN pd between 6450 and 6999 then '07-MP2.2'
        WHEN pd between 7000 and 7854 then '08-MP3'
        WHEN pd between 7855 and 8999 then '09-MP4'
        WHEN pd between 9000 and 11000 then '10-MP5'
            WHEN pd between 100000 and 11000000 then '11-TREAT'
      END as podTot 
      from (select podId as pd from pod_debug where mcuMoistLev1 < 65535 group by podId) as b
      group by podTot


    ) as addition
    on podTot = podCounts
    ''')

    myresult = mycursor.fetchall()
    parsedData = []
    for row in myresult:
        r = []
        for cell in row:
            if(isinstance(cell,float)):
                c = str(cell)[0:5]
                r.append(c)
            else:
                r.append(cell)
        parsedData.append(r)
    return parsedData

def getQuery1():
    description = "This is the table description"
    headers = ['Header 1', 'Header 2', 'Header 3', 'Header 4']
    data = query()
    q = {'data':data,'headers':headers, 'description':description}
    return q