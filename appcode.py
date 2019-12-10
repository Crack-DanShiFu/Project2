import csv
import sqlite3


# Packaging can be with value
def makeDictionary(headers, data):
    dict = {}
    for i in range(len(headers)):
        dict[headers[i]] = data[i]
    return dict


# This is the function to read the database
def readDataFromLiteDB(sql='SELECT Year, Quarter, Region, Species, Grade, Pond_Value, Number_of_Quotes FROM Log_Prices'):
    conn = sqlite3.connect('Data.db')
    c = conn.cursor()
    cursor = c.execute(sql)
    data = []
    headers = ['Year', 'Quarter', 'Region', 'Species', 'Grade', 'Pond_Value', 'Number_of_Quotes']
    for row in cursor:
        data.append(makeDictionary(headers, list(row)))
    return data


# The method requested when the page loads
def init_server_data():
    rawData = readDataFromLiteDB()
    year_list, Region_list, Species_list = {}, {}, {}
    for r in rawData:
        if year_list.get(r['Year']):
            year_list[r['Year']] += 1
        else:
            year_list[r['Year']] = 1
        if Region_list.get(r['Region'].strip()):
            Region_list[r['Region'].strip()] += 1
        else:
            Region_list[r['Region'].strip()] = 1
        if Species_list.get(r['Species']):
            Species_list[r['Species']] += 1
        else:
            Species_list[r['Species']] = 1
    return [year_list, Region_list, Species_list]


# Provide database query method
def getLogData(data):
    sql = 'SELECT Year, Quarter, Region, Species, Grade, Pond_Value, Number_of_Quotes FROM Log_Prices WHERE 1=1 '
    if data:
        if data[0] != '':
            sql += ' AND Year LIKE "%' + str(data[0]) + '%"'
        if data[2] != '':
            sql += ' AND Region LIKE "%' + str(data[1]) + '%"'
        if data[3] != '':
            sql += ' AND Species LIKE "%' + str(data[2]) + '%"'
    sql += ' ORDER BY "Year" '
    if data and data[3] != '':
        sql += ' limit ' + data[3] + ' offset 0'
    print(sql)
    return readDataFromLiteDB(sql)
