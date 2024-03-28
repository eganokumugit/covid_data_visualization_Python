#!/usr/bin/python3.8
import cgitb,cgi,sys
import pandas as pd
cgitb.enable()
radioval = str(sys.argv[1])
fname = sys.argv[2]
df = pd.read_csv("../../CPS4745/proj1/uploads/" + fname, usecols=['state','positive','death','date'])
if(radioval[0] == "D"):
    lnd = df[['date','death']]
    lnd = lnd.groupby('date',as_index=False).agg({'death':'sum'}).dropna().reset_index(drop = True)
    tickarr = lnd['date'].to_numpy()
    deathval = lnd['death'].to_numpy()
    
    print("google.charts.load('current',{packages:['corechart','line']});")
    print("google.charts.setOnLoadCallback(deathLine);\n")
    print("function deathLine(){\n")
    print("var data = new google.visualization.DataTable();\n")
    print("data.addColumn('string','Date');\n")
    print("data.addColumn('number','Deaths');\n")
    for i in lnd.index:
        print("data.addRow(['" + str(tickarr[i]) + "', " + str(deathval[i]) + "]);\n")
    
    print("var options = {\n")
    print("title: 'Covid Death Totals Over Time',\n")
    print("width:900,\n")
    print("height:600,\n")
    print("legend: {position:'none'},\n")
    print("lineWidth: 5,\n")
    print("colors:['red'],\n")
    print("hAxis:{title:'Date'},\n")
    print("vAxis:{title:'Total Deaths'}")
    print("};\n")
    
    print("var chart = new google.visualization.LineChart(document.getElementById('plotdiv'));")
    print("chart.draw(data, google.charts.Line.convertOptions(options));")
    print("}")

elif(radioval[0] == "C"):
    lnd = df[['date','positive']]
    lnd = lnd.groupby('date',as_index=False).agg({'positive':'sum'}).dropna().reset_index(drop = True)
    tickarr = lnd['date'].to_numpy()
    caseval = lnd['positive'].to_numpy()
    
    print("google.charts.load('current',{packages:['corechart','line']});")
    print("google.charts.setOnLoadCallback(casesLine);\n")
    print("function casesLine(){\n")
    print("var data = new google.visualization.DataTable();\n")
    print("data.addColumn('string','Date');\n")
    print("data.addColumn('number','Cases');\n")
    for i in lnd.index:
        print("data.addRow(['" + str(tickarr[i]) + "', " + str(caseval[i]) + "]);\n")
    
    print("var options = {\n")
    print("title: 'Positive Covid Cases Over Time',\n")
    print("width:900,\n")
    print("height:500,\n")
    print("legend: {position:'none'},\n")
    print("lineWidth: 7,\n")
    print("colors:['red'],\n")
    print("hAxis:{title:'Date'},\n")
    print("vAxis:{title:'Total Cases'}")
    print("};\n")
    
    print("var chart = new google.visualization.LineChart(document.getElementById('plotdiv'));")
    print("chart.draw(data, google.charts.Line.convertOptions(options));")
    print("}")
else:
   print("clearPlot();")
   print("$('.fileresult').css('border-left-color','red');")
   print("$('.resultmessage').html('<font color=red>This option can't be plotted as a line chart!</font>');")
