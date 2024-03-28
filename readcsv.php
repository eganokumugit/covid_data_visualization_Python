<?php 
	
	$filename = $_POST['fileName'];
	
	/*
		The following code will populate the table created in the callphp() function in jslinks/functions.js 
		This php script will not be called until the uploaded file has already been accepted in that js file.
	*/
	$openfile = fopen("uploads/$filename",'r') or die("Unable to open file!");
	//Skip header of the csv file
	fgetcsv($openfile,10000,",");
	$rowcount = shell_exec("wc -l uploads/$filename");
	$rowcount = intval(substr($rowcount,0,strpos($rowcount,' ')));
	while(($line = fgetcsv($openfile,10000,',')) !== FALSE)
	{
		echo "data.addRow(['$line[1]', $line[19], $line[21], $line[3], $line[4], $line[31], $line[6], '$line[0]']);\n"; 
	}

	echo "var tbl = new google.visualization.Table(document.getElementById('tbl'));\n";
	echo "tbl.draw(data,{showRowNumber:true, page:'enable', pageSize:30, width: '100%', height: '100%'});\n";
	echo "}";
	echo "$('.fileresult').css('border-left-color','#1fd655');";
	echo "$('#view').show();";
	echo "$('#showleft').show();";
	fclose($openfile);
	//CLOSE THE FILE PLEASE
	
?>
