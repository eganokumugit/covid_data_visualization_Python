#!/usr/bin/python3.8
import cgitb,cgi,sys
import pandas as pd
cgitb.enable()
radioval = str(sys.argv[1])
fname = sys.argv[2]
df = pd.read_csv("../../CPS4745/proj1/uploads/" + fname, usecols=['state','positive','negative','death','date','totalTestResults'])
if(radioval[0] == "D"):
    brd = df[['date','death']]
    brd = brd.groupby('date',as_index=False).agg({'death':'sum'}).dropna().reset_index(drop = True)
    tickarr = brd['date'].to_numpy()
    deathval = brd['death'].to_numpy()
    
    print("google.charts.load('current',{packages:['corechart']});")
    print("google.charts.setOnLoadCallback(deathBar);\n")
    print("function deathBar(){\n")
    print("var data = new google.visualization.DataTable();\n")
    print("data.addColumn('string','Date');\n")
    print("data.addColumn('number','Deaths');\n")
    for i in brd.index:
        print("data.addRow(['" + str(tickarr[i]) + "', " + str(deathval[i]) + "]);\n")
    
    print("var options = {\n")
    print("title: 'Covid Death Totals Over Time',\n")
    print("width:1200,\n")
    print("height:500,\n")
    print("legend:{position:'none'},\n")
    print("hAxis:{title:'Date'},\n")
    print("vAxis:{title:'Total Deaths'}\n")
    print("};\n")
    
    print("var chart = new google.visualization.ColumnChart(document.getElementById('plotdiv'));")
    print("chart.draw(data,options);")
    print("}")

elif(radioval[0] == "C"):
    brc = df[['date','positive']]
    brc = brc.groupby('date',as_index=False).agg({'positive':'sum'}).dropna().reset_index(drop = True)
    tickarr = brc['date'].to_numpy()
    caseval = brc['positive'].to_numpy()
    
    print("google.charts.load('current',{packages:['corechart']});")
    print("google.charts.setOnLoadCallback(casesBar);\n")
    print("function casesBar(){\n")
    print("var data = new google.visualization.DataTable();\n")
    print("data.addColumn('string','Date');\n")
    print("data.addColumn('number','Cases');\n")
    for i in brc.index:
        print("data.addRow(['" + str(tickarr[i]) + "', " + str(caseval[i]) + "]);\n")
    
    print("var options = {\n")
    print("title: 'Positive Covid Cases Over Time',\n")
    print("width:1200,\n")
    print("height:500,\n")
    print("legend:{position:'none'},\n")
    print("hAxis:{title:'Date'},\n")
    print("vAxis:{title:'Total Cases'}\n")
    print("};\n")
    
    print("var chart = new google.visualization.ColumnChart(document.getElementById('plotdiv'));")
    print("chart.draw(data, options);")
    print("}")
elif(radioval[0] == "S"):
    brs = df.loc[df['date'] == df['date'].max(),['state','positive','negative','totalTestResults'] ]
    tickarr = brs['state'].to_numpy()
    posval = brs['positive'].to_numpy()
    negval = brs['negative'].fillna(0).astype('int').to_numpy()
    tstval = brs['totalTestResults'].to_numpy()
    print("google.charts.load('current',{packages:['bar']});")
    print("google.charts.setOnLoadCallback(statesBar);\n")
    print("function statesBar(){\n")
    print("var data = new google.visualization.DataTable();\n")
    
    print("data.addColumn('string','State');\n")
    print("data.addColumn('number','Total Tests');\n")
    print("data.addColumn('number','Negative Results');\n")
    print("data.addColumn('number','Positive Cases');\n")
    for i in brs.index:
        print("data.addRow(['" + str(tickarr[i]) + "', " + str(tstval[i]) + ',' + str(negval[i]) + ',' + str(posval[i])  + "]);\n")
    
    print("var options = {\n")
    print("chart:{title: 'Covid Statistics By State/Territory'},\n")
    print("width:2000,\n")
    print("height:600,\n")
    print("isStacked: true,\n")
    print("hAxis:{title:'State'}\n")
    print("};\n")
    
    print("var chart = new google.charts.Bar(document.getElementById('plotdiv'));\n")
    print("chart.draw(data, options);\n")
    print("}")
else:
   print("clearPlot();")
   print("$('.fileresult').css('border-left-color','red');")
   print("$('.resultmessage').html('<font color=red>This option can't be plotted as a bar chart!</font>');")
