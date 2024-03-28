#!/usr/bin/python3.8
import cgitb,cgi,sys
import pandas as pd
cgitb.enable()
radioval = str(sys.argv[1])
fname = str(sys.argv[2])
date = str(sys.argv[3])
df = pd.read_csv("../../CPS4745/proj1/uploads/" + fname, usecols=['state','positive','death','date'])
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

df = df.rename(columns={'index':'abbr'})
df.to_csv('./uploads/map.csv', sep=',', index=False)
if(radioval[0] == "D"):
    zmax = df['death'].max()
    zmin = df['death'].min()
    print("d3.csv('./uploads/map.csv',function(err,rows){")
    print("function unpack(rows,key){")
    print("return rows.map(function(row){")
    print("return row[key];});}")
    print("var data = [{\n")
    print("type: 'choropleth',\n")
    print("locationmode: 'USA-states',\n")
    print("locations: unpack(rows,'abbr'),\n")
    print("z: unpack(rows,'death'),\n")
    print("text: unpack(rows,'Name') ,\n")
    print("zmin:" + str(zmin) + ",\n")
    print("zmax:" + str(zmax) + ",\n")
    print("colorscale:'Jet',\n")
    print("colorbar:{title:'Deaths', thickness:20},\n")
    print("marker:{line:{color:'rgb(0,0,0)',width:2}}")
    print("}];\n")

    print("var layout={\n")
    print("title: 'Total Covid Deaths By State As Of " + str(date) + "',\n")
    print("height: 700,\n")
    print("width: 2000,\n")
    print("geo:{scope:'usa',showlakes:true,lakecolor: 'rgb(25,55,255)'}\n")
    print("};\n")

    print("Plotly.newPlot('plotdiv',data,layout,{showLink:false});")
    print("});")
elif(radioval[0]=="C"):
    zmax = df['positive'].max()
    zmin = df['positive'].min()
    print("d3.csv('./uploads/map.csv',function(err,rows){")
    print("function unpack(rows,key){")
    print("return rows.map(function(row){")
    print("return row[key];});}")
    print("var data = [{\n")
    print("type: 'choropleth',\n")
    print("locationmode: 'USA-states',\n")
    print("locations: unpack(rows,'abbr'),\n")
    print("z: unpack(rows,'positive'),\n")
    print("text: unpack(rows,'Name') ,\n")
    print("zmin:" + str(zmin) + ",\n")
    print("zmax:" + str(zmax) + ",\n")
    print("colorscale: 'Jet',\n")
    #print("reversescale: true,\n")
    print("colorbar:{title:'Cases', thickness:30},\n")
    print("marker:{line:{color:'rgb(0,0,0)',width:2}}")
    print("}];\n")

    print("var layout={\n")
    print("title: 'Total Covid Cases By State As Of " + str(date) + "',\n")
    print("height: 700,\n")
    print("width: 2000,\n")
    print("geo:{scope:'usa',showlakes:true,lakecolor: 'rgb(25,55,255)'}\n")
    print("};\n")

    print("Plotly.newPlot('plotdiv',data,layout,{showLink:false});")
    print("});")
else:
   print("clearPlot();")
   print("$('.fileresult').css('border-left-color','red');")
   print("$('.resultmessage').html('<font color=red>This option can't be plotted as a chorpleth map!</font>');")
