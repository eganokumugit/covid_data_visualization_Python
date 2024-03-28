#!/usr/bin/python3.8
import cgitb,cgi,sys
import pandas as pd
cgitb.enable()
radioval = str(sys.argv[1])
fname = str(sys.argv[2])
date = str(sys.argv[3])
df = pd.read_csv("../../CPS4745/proj1/uploads/" + fname, usecols=['state','positive','date'])
if(len(df[df.date == date]) > 0):
    df = df[df.date == date]
else:
    if(df.date.min() > date):
        df = df[df.date == df.date.min()]
        date = df.date.min()
    elif(df.date.max() < date):
        df = df[df.date == df.date.max()]
        date = df.date.max()

if(radioval[0] == "S"):
    brs = df[['state','positive']].sort_values(by=['positive'],ascending=False).reset_index(drop=True)
    statearr = brs['state'].to_numpy()
    posval = brs['positive'].to_numpy()
    print("google.charts.load('current',{packages:['corechart']});")
    print("google.charts.setOnLoadCallback(statesPie);\n")
    print("function statesPie(){\n")
    print("var data = new google.visualization.arrayToDataTable([\n")
    print("['State', 'Deaths'],")
    
    for i in brs.index:
        print("['"+ str(statearr[i]) + "'," + str(posval[i]) + "],\n")
    print("]);\n")
    print("var options = {\n")
    print("title: 'Covid Cases By State/Territory(%) As Of ' + '" + str(date) + "',\n")
    #print("is3D: true,")
    print("pieSliceText:'label',")
    print("pieStartAngle:270,")
    print("width:2000,")
    print("height:700,\n")
    print("}\n")
 

    
    print("var chart = new google.visualization.PieChart(document.getElementById('plotdiv'));")
    print("chart.draw(data, options);")
    print("};")
else:
   print("clearPlot();")
   print("$('.fileresult').css('border-left-color','red');")
   print("$('.resultmessage').html('<font color=red>This option can't be plotted as a pie chart!</font>');")

