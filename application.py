from flask import Flask, flash, jsonify, redirect, render_template, request, session
import os
import mysql.connector
import pandas as pd 
import numpy as np 




application = Flask(__name__)

@application.route('/')
def index():
    print("something is working at least")
    return render_template("index.html")

@application.route("/submitnpi", methods=["POST"])
def submitnpi():
    
    #Set up mysql connection
    mydb = mysql.connector.connect(
    host="databaseinstanceprod.cnxrcmkisyr9.us-east-2.rds.amazonaws.com",
    user="omuakkas",
    passwd="B!llingXray123"
    )
    mycursor = mydb.cursor()

    #Use correct database
    mycursor.execute("USE xray")
    
    #Query to get detailed information (by CPT code, by year, for each NPI number)
    sql = "SELECT year, hcpcs_code, hcpcs_description, average_Medicare_allowed_amt, line_srvc_cnt, (average_Medicare_allowed_amt * line_srvc_cnt) as dollars FROM medicare_data_xray_allyrs WHERE NPI=%s GROUP BY year, hcpcs_code"
    npi =  request.form.get("npi")
    mycursor.execute(sql,(npi,))
    
    
    #Record NPI and datestamp for analytics purposes
    sql = "INSERT INTO prodanalytics"
    
    #Store (as list of tuples)
    sql_extract_detail = mycursor.fetchall()

    #Convert to DataFrame
    df = pd.DataFrame(sql_extract_detail, columns=["year", "cpt", "cpt_desc", "avg_amt", "count", "total_amt"])

    #Query for provider name
    sql = "SELECT nppes_provider_first_name as first, nppes_provider_mi as middle, nppes_provider_last_org_name as last FROM medicare_data_xray_allyrs WHERE NPI=%s LIMIT 1"
    mycursor.execute(sql,(npi,))

    #Store full name
    provname = mycursor.fetchall()
    
    #If no provider name found (i.e. the entered NPI number is not valid), then go to apology page
    if not provname:
        return render_template("npierror.html")

    #Summarize by years
    total_amt_detail = df.pivot(index ='cpt', columns ='year', values =["total_amt"]) 
    print(total_amt_detail)
    
    #Get total by year
    total_amt_row = total_amt_detail.sum(skipna=True) 

    #Initialize list to store CPT codes and key value pair index (for eventual use in index)
    cptlist = []
    cptdesclist = []

    #Create list of CPT codes
    for row in total_amt_detail.index: 
        cptlist.append(row)

    #Iterate over each unique CPT code in the list
    for i in range(len(cptlist)):
        #For each one, look through the SQL extract, which contains one-to-many mapping of CPT codes and descriptions
        for j in range(len(sql_extract_detail)):
            #If the CPT code from the unqiue file matches one that's int he SQL file, create a key value pair, and then break to move on to the next item in the CPT list
            if sql_extract_detail[j][1] == cptlist[i]:
                x = [cptlist[i], sql_extract_detail[j][2]]
                cptdesclist.append(x)
                break

        print (cptdesclist)
    
    #Get years and put into a list (for the column headers)
    years = []
    for col in total_amt_detail.columns: 
        years.append(col[1])
    
    
    #Reformat Dataframes into Lists so that it can work with Jinja on the front-end
    total_amt_detail = total_amt_detail.values.tolist()
    total_amt_row = total_amt_row.values.tolist()
    
    #Replace "nan" with zeros
    for i in range(len(total_amt_detail)):
        for j in range(len(total_amt_detail[i])):
            if np.isnan(total_amt_detail[i][j]):
                    total_amt_detail[i][j] = 0

    for i in range(len(total_amt_row)):
        if np.isnan(total_amt_row[i]):
            total_amt_row[i] = 0
    
    #Record search for analytics purposes        
    sql = "INSERT INTO prodanalytics (npisearch) VALUES (%s)"
    mycursor.execute(sql,(npi,))
    mydb.commit()

    return render_template("results.html", total_amt_detail = total_amt_detail, cptdesclist = cptdesclist, total_amt_row = total_amt_row, provname = provname, years=years)
    
if __name__ == '__main__':
    application.debug = True
    #app.run(host='IP',port='PORT')
    application.run()
    
    
    