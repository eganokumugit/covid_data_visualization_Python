<?php
	include("dbconfig.php");
	$con = mysqli_connect($host,$username,$password,$name) or die("Cannot Connect to DB!");
	$usr = $_POST['username'];
	$pswd = $_POST['password'];


	$usr = stripcslashes($usr);
	$usr = mysqli_real_escape_string($con, $usr);

	$pswd = stripcslashes($pswd);
	$pswd = mysqli_real_escape_string($con, $pswd);
	
	$sql = "select uid, name,gender from datamining.DV_User where login='$usr' and password='$pswd';";
	$result = mysqli_query($con, $sql);
	if(mysqli_num_rows($result) == 0)
	{
		$usrsql = "select * from datamining.DV_User where login='$usr';";
		$usrcheck = mysqli_query($con,$usrsql);
		if(mysqli_num_rows($usrcheck) == 1)
		{

			echo "$('.fileresult').css('border-left-color','red');";
			echo "$('#resultmessage').html('<font color=red>Your login <u>$usr</u> is correct but your password is incorrect!</font>');\n";
			echo "openForm();\n";
		}
		else
		{
			echo "$('.fileresult').css('border-left-color','red');";
			echo "$('#resultmessage').html('<font color=red>The login <u>$usr</u> does NOT exist in the database!</font>');\n";
			echo "openForm();\n";
		}
	}
	else
	{
		$usrinfo = mysqli_fetch_array($result);
		$uid = $usrinfo['uid'];
		$name = $usrinfo['name'];
		$gender = $usrinfo['gender'];


		setcookie('uid',$uid ,time() + 6400);
		setcookie('login',$usr ,time() + 6400);
		setcookie('password',$pswd ,time() + 6400);
		setcookie('name',$name ,time() + 6400);
		setcookie('gender',$gender ,time() + 6400);
		
		echo "$('.fileresult').css('border-left-color','#1fd655');";
		echo "$('#resultmessage').html('<font color=#1fd655>Welcome back <b>$name</b>!</font>');\n";
		echo "closeForm();\n";
		echo "$('#logon').hide();\n";
		echo "$('#logout').show();\n";
		echo "$('#settings').show();\n";
		
	}
?>
