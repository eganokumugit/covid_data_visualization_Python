var loggedIn = false;
function callphp()
{
	var file_data = $("#fileUpload").prop("files")[0];
	var form_data = new FormData();
	var filename = $("#fileUpload")[0].files[0].name.toString();
	var fileext = filename.substring(filename.length - 3).toLowerCase();
	var filesize = $("#fileUpload")[0].files[0].size;
	if(fileext !== "csv")
	{
		   $("#resultmessage").html("<font color='red'>File is in wrong format, only CSV format is allowed! Upload FAILED!</font>");
		   clearTable();
		   clearPlot();
		   $('.fileresult').css('border-left-color','red');
	}
	else if(filesize > 2000000)
	{
		$("#resultmessage").html("<font color='red'>ERROR! Only files 2MB and below  are allowed! Upload FAILED!</font>");
		clearTable();
		clearPlot()
		$('.fileresult').css('border-left-color','red');
	}
	else
	{
		clearTable();
		clearPlot();
		form_data.append("file",file_data);
		$.ajax({
			   url:"uploadfile.php",
				dataType: "text",
				data: form_data,
				type: 'post',
				processData: false,
				contentType: false,
				success: function(response)
				{

					$('.fileresult').css('border-left-color','red');
					$("#resultmessage").html(response);
					$("#ggltbl").append("google.charts.load('current',{'packages':['table']});");
					$("#ggltbl").append("google.charts.setOnLoadCallback(drawTable);");
					$("#ggltbl").append("function drawTable(){");
						   $("#ggltbl").append("var data = new google.visualization.DataTable();");
						   $("#ggltbl").append("data.addColumn('string','State');");
						   $("#ggltbl").append("data.addColumn('number','Total Cases');");
						   $("#ggltbl").append("data.addColumn('number','New Cases');");
						   $("#ggltbl").append("data.addColumn('number','Total Deaths');");
						   $("#ggltbl").append("data.addColumn('number','New Deaths');");
						   $("#ggltbl").append("data.addColumn('number','Total Tests');");
						   $("#ggltbl").append("data.addColumn('number','Hospitalizations');");
						   $("#ggltbl").append("data.addColumn('string','date');");
						   populateTable(filename);
					//Adding radio buttons to the 
				}

		});

	}
	
}
function populateTable(fileName)
{
	$.ajax({
		url:"readcsv.php",
		dataType: "text",
		data: {fileName : fileName},
		type: 'POST',
		cache: false,
		success: function(response)
		{
					
			$("#ggltbl").append(response);
			eval(document.getElementById('ggltbl').innerHTML);
		}
	});
}

function openForm() 
{
  document.getElementById("myForm").style.display = "block";
}

function closeForm() 
{
  document.getElementById("myForm").style.display = "none";
}
function checkLogin()
{
	$.ajax({
			url:"verifylogin.php",
			dataType: "text",
			data: {username: $("#username").val(), password: $("#password").val()},
			type: 'POST',
			cache: false,
			success: function(response)
			{

				$("#delnav").append(response);
				eval(document.getElementById('delnav').innerHTML);
			}

		});
}
function logout()
{
	if(confirm("Are you sure you want to log out?"))
	{
		$.ajax({
			url:"logout.php",
			dataType: "text",
			type: 'POST',
			cache: false,
			success: function(response)
			{
				//This will bring back the login button on the navbar. It just makes more sense to only be able to
				//logout when you're logged in and vice versa.
				$("#addnav").append(response);
				eval(document.getElementById('addnav').innerHTML);
				clearPlot();
				clearTable();
				location.reload();
			}

		});
	}
}
function info()
{
	alert("INFO:\n_____________________________________\nName: Egan Okumu\nClass ID: CPS4745*01\nDue Date: October 26th, 2022");
}
function usrInfo()
{
	$.ajax({
			url:"usrinfo.php",
			dataType: "text",
			type: 'POST',
			cache: false,
			success: function(response)
			{
				alert(response);
			}

	})

}
function clientInfo()
{
	$.ajax({
			url:"clinfo.php",
			dataType: "text",
			type: 'POST',
			cache: false,
			success: function(response)
			{
				let javaCheck;
				//Memory size: 8GB

				var usrOS = "Not known";
				let memSize = navigator.deviceMemory;
				let heapLim = Math.round(performance.memory.jsHeapSizeLimit / Math.pow(1000,3 ) * 100) / 100;	
				let heapSize = Math.round(performance.memory.totalJSHeapSize / Math.pow(1000, 2) * 100) / 100;	
				let heapUsed = Math.round(performance.memory.usedJSHeapSize / Math.pow(1000, 2) * 100) / 100;	


				if (navigator.appVersion.indexOf("Win") != -1) {usrOS = "Windows OS";}
				else if (navigator.appVersion.indexOf("Mac") != -1) {usrOS = "Mac OS";}
				else if (navigator.appVersion.indexOf("X11") != -1) {usrOS = "UNIX OS";}
				else if (navigator.appVersion.indexOf("Linux") != -1) {usrOS = "Linux OS";}
				if(navigator.javaEnabled())
				{
					javaCheck = "Java: Enabled";
				}
				else
				{
					javaCheck = "Java: Turned Off";
				}

				alert(response + javaCheck + "\nPlatform: " + usrOS + "\nMemory Size: " + memSize + "\nJS Heap Size Limit: " + heapLim + "GB\n" + "JS Total Heap Size: " + heapSize + "MB\n" + "JS Current Tab Usage: " + heapUsed + "MB");
			}

	});

}
function closeTab()
{
	if(confirm("Are you sure you want to exit the page? You will be logged out and the tab will close.") == true)
	{
		$.ajax({
			url:"logout.php",
			dataType: "text",
			type: 'POST',
			cache: false,
			success: function(response)
			{
				//This will bring back the login button on the navbar. It just makes more sense to only be able to
				//logout when you're logged in and vice versa.
				$("#resultmessage").html("<font color=#1fd655>Until next time!</font>");
				clearPlot();
				clearTable();
				window.opener = self;
				window.close();
			}

		});
	}
}

function linePlot()
{
	var fileName = $("#fileUpload")[0].files[0].name.toString();
	var radioVal = $("input[name='charttype']:checked").val();
	var pickedPlot = "line";
	clearPlot();
	if(tableIsEmpty() == false)
	{
		if(radioVal.includes("Line"))
		{
			pickPlot(pickedPlot, radioVal, fileName);
		}
		else
		{
			$('.fileresult').css('border-left-color','red');
			$('#resultmessage').html("<font color=red>Selected chart doesn't support line charts!</font>");		
		}
	}
	else
	{
		   alert("Please load data first, there's nothing to plot!");
	}
}
function barPlot()
{
	var fileName = $("#fileUpload")[0].files[0].name.toString();
	var radioVal = $("input[name='charttype']:checked").val();
	var pickedPlot = "bar";
	clearPlot();
	if(tableIsEmpty() == false)
	{
		if(radioVal.includes("Bar"))
		{
			pickPlot(pickedPlot, radioVal, fileName);	
		}
		else
		{
			$('.fileresult').css('border-left-color','red');
			$('#resultmessage').html("<font color=red>Selected chart doesn't support line charts!</font>");		
		}
	}
	else
	{
		   alert("Please load data first, there's nothing to plot!");
	}
}
function histPlot()
{
	var fileName = $("#fileUpload")[0].files[0].name.toString();
	var radioVal = $("input[name='charttype']:checked").val();
	var pickedPlot = "histogram";
	var date = $("input[name='date']").val();
	clearPlot();
	if(tableIsEmpty() == false)
	{
		if(radioVal.includes("Histogram"))
		{
			pickPlot(pickedPlot, radioVal, fileName,date);		
		}
		else
		{
			$('.fileresult').css('border-left-color','red');
			$('#resultmessage').html("<font color=red>Selected chart doesn't support histogram charts!</font>");		
		}
	}
	else
	{
		   alert("Please load data first, there's nothing to plot!");
	}
}
function geoPlot()
{
	var fileName = $("#fileUpload")[0].files[0].name.toString();
	var radioVal = $("input[name='charttype']:checked").val();
	var pickedPlot = "map";
	var date = $("input[name='date']").val();
	clearPlot();
	if(tableIsEmpty() == false)
	{
		if(radioVal.includes("Map"))
		{
			pickPlot(pickedPlot, radioVal, fileName,date);		

		}
		else
		{
			$('.fileresult').css('border-left-color','red');
			$('#resultmessage').html("<font color=red>Selected chart doesn't support map charts!</font>");		
		}
	}
	else
	{

		$('.fileresult').css('border-left-color','red');
		$('#resultmessage').html("<font color=red>Selected chart doesn't support map charts!</font>");	
		clearPlot();
	}
}

function piePlot()
{
	var fileName = $("#fileUpload")[0].files[0].name.toString();
	var radioVal = $("input[name='charttype']:checked").val();
	var pickedPlot = "pie";
	var date = $("input[name='date']").val();
	clearPlot();
	if(tableIsEmpty() == false)
	{
		if(radioVal.includes("Pie"))
		{
			pickPlot(pickedPlot, radioVal, fileName,date);		
		}
		else
		{
			$('.fileresult').css('border-left-color','red');
			$('#resultmessage').html("<font color=red>Selected chart doesn't support pie charts!</font>");		
		}
	}
	else
	{

		$('.fileresult').css('border-left-color','red');
		$('#resultmessage').html("<font color=red>Selected chart doesn't support pie charts!</font>");	
		clearPlot();
	}
}
function pickPlot()
{
	switch(arguments.length)
	{
		   case 3:
			$.ajax({
				url:"pickplot.php",
				dataType: "text",
				data: {pickedPlot: arguments[0], radioVal: arguments[1],fileName: arguments[2]},
				type: 'POST',
				cache: false,
				success: function(response)
				{
					$('#plotdiv').css('height','auto');
					$('#plotscript').append(response);
					eval(document.getElementById('plotscript').innerHTML);
					$('.fileresult').css('border-left-color','1fd655');
					$('#resultmessage').html("<font color=1fd655>Plot Successful!</font>");
				}

			});
			break;
			case 4:
			$.ajax({
				url:"pickplot.php",
				dataType: "text",
				data: {pickedPlot: arguments[0], radioVal: arguments[1],fileName: arguments[2],date: arguments[3]},
				type: 'POST',
				cache: false,
				success: function(response)
				{
					$('#plotdiv').css('height','auto');
					$('#plotscript').append(response);
					eval(document.getElementById('plotscript').innerHTML);
					$('.fileresult').css('border-left-color','1fd655');
					$('#resultmessage').html("<font color=1fd655>Plot Successful!</font>");
				}

			});
			break;
			default:
				$('#resultmessage').html("<font color=red>ERROR</font>");
				break;

	}
}
function tableIsEmpty()
{
	//The idea behind this stems from me noticing that
	//upon the table being drawn by the google API, the
	//script tag I placed in this div is replaced by the table
	//data. If this script tag is there, then the google table is not
	//there, and nothing can be plotted.
	const tbldiv = document.getElementById("tbl");
	const ggltbl = document.getElementById("ggltbl");
	var isEmpty;
	if(tbldiv.contains(ggltbl))
	{
		isEmpty = true;
	}
	else
	{
		isEmpty = false;
	}

	return isEmpty;
}

function clearPlot()
{
	$("#plotdiv").html('');
	$("#plotdiv").append('<script id=plotscript></script>');

	$('#plotdiv').css('height','280px');
}

function clearTable()
{
	$("#tbl").html('');
	$("#tbl").append('<script id=ggltbl></script>');
	$('#view').hide();
	$('#showleft').hide();
}
