import json
import os.path
import requests
import sqlite3


#
# This file is used to get json data and write it to the database, just run it
#
#
def loadData():
    uri = "https://data.oregon.gov/api/views/4v4m-wr5p/rows.json?accessType=DOWNLOAD"
    response = requests.get(uri)
    content = json.loads(response.text)
    data = []
    for r in content['data']:
        data.append(
            [r[8].strip(), r[9].strip(), r[10].strip(), r[11], r[12], r[13], r[14]])
    insertToDB(data)


def insertToDB(data):
    conn = None
    c = None
    if not os.path.exists('Data.db'):
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()
        c.execute('create table Log_Prices ('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT  , '
                  'Year varchar(10) ,'
                  'Quarter varchar(50) ,'
                  'Region varchar(100) ,'
                  'Species varchar(50) ,'
                  'Grade varchar(50) ,'
                  'Pond_Value varchar(50) ,'
                  'Number_of_Quotes varchar(50)'
                  ')')
    else:
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()
    sql = 'insert into Log_Prices(Year, Quarter, Region, Species, Grade, Pond_Value, Number_of_Quotes) values(?,?,?,?,?,?,?)'
    print(data)
    cursor = c.executemany(sql, data)
    conn.commit()
    return data


if __name__ == '__main__':
    # loadData()
    pass
