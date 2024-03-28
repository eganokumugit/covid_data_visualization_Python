<?php
	$radioval = $_POST['radioVal'];
	$fileName = $_POST['fileName'];
	$pickedPlot = $_POST['pickedPlot'];

	if($pickedPlot == 'bar')
	{
		$result = shell_exec("python3 ../../cgi-bin/CPS4745/barplot.cgi " . $radioval  . ' '  . $fileName);
		echo $result;
	}
	else if($pickedPlot == 'line')
	{
		$result = shell_exec("python3 ../../cgi-bin/CPS4745/lineplot.cgi " . $radioval  . ' '  . $fileName);
		echo $result;
	}
	else if($pickedPlot == 'histogram')
	{
		$date = $_POST['date'];
		$result = shell_exec("python3 ../../cgi-bin/CPS4745/histplot.cgi " . $radioval  . ' '  . $fileName . ' ' . "'$date'");
		echo $result;
	}
	else if($pickedPlot == 'pie')
	{
		$date = $_POST['date'];
		$result = shell_exec("python3 ../../cgi-bin/CPS4745/pieplot.cgi " . $radioval  . ' '  . $fileName . ' ' . "'$date'");
		echo $result;
	}
	else if($pickedPlot == 'map')
	{
		$date = $_POST['date'];
		$result = shell_exec("python3 ../../cgi-bin/CPS4745/geomap.cgi " . $radioval  . ' '  . $fileName . ' ' . "'$date'");
		echo $result;
	}
	else
	{
		echo "$('#fileresult').html(<font red>Plot doesn't exist!</font>);";
	}
?>
