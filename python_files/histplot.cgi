#!/usr/bin/python3.8
import cgitb,cgi,sys
import pandas as pd
cgitb.enable()
radioval = str(sys.argv[1])
fname = str(sys.argv[2])
date = str(sys.argv[3])
df = pd.read_csv("../../CPS4745/proj1/uploads/" + fname, usecols=['state','hospitalized','date'])

if(len(df[df.date == date]) > 0):
    df = df[df.date == date]
else:
    if(df.date.min() > date):
        df = df[df.date == df.date.min()]
        date = df.date.min()
    elif(df.date.max() < date):
        df = df[df.date == df.date.max()]
        date = df.date.max()
df = df[~df.state.isin(['GU','PR','AS','MP','VI'])].reset_index(drop=True)
abbr = pd.read_csv("../../CPS4745/proj1/uploads/stateabbr.csv")

df = pd.concat([df.set_index('state'),abbr.set_index('Abbr')],axis=1, join='inner').reset_index()

if(radioval[0] == "S"):
    brs = df[['Name','hospitalized']].dropna(subset=['hospitalized']).sort_values(by=['hospitalized']).reset_index(drop=True)
    statearr = brs['Name'].to_numpy()
    hospval = brs['hospitalized'].to_numpy()
    print("google.charts.load('current',{packages:['corechart']});")
    print("google.charts.setOnLoadCallback(statesHist);\n")
    print("function statesHist(){\n")
    print("var data = new google.visualization.arrayToDataTable([\n")
    print("['State', 'Cases'],")
    
    for i in brs.index:
        print("['"+ str(statearr[i]) + "'," + str(hospval[i]) + "],\n")
    print("]);\n")
    print("var options = {\n")
    print("title: 'Hospitalizations By State As Of ' + '" + str(date) + " (States with missing values not included.)',\n")
    print("legend:{position:'none'},")
    print("width:2000,")
    print("height:700,\n")
    print("hAxis:{title:'Hospitalizations'},\n")
    print("vAxis:{title:'State Count'}\n")
    print("}\n")
 

    
    print("var chart = new google.visualization.Histogram(document.getElementById('plotdiv'));")
    print("chart.draw(data, options);")
    print("};")
else:
   print("clearPlot();")
   print("$('.fileresult').css('border-left-color','red');")
   print("$('.resultmessage').html('<font color=red>This option can't be plotted as a histogram chart!</font>');")

