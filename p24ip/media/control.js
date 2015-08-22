function submit(sensor_id, s_repl)
{
	sensor_value = document.getElementById('s'+s_repl).value;
	
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{if (xmlhttp.readyState==4) 
		{
			if (xmlhttp.responseText == 'OK')
					alert('Ustawiono, poczekaj na odświeżenie');
			else alert(xmlhttp.responseText);
		}
	}
	var url="/device/sensors/control/ajax/?method=write&sid="+sensor_id+"&value="+sensor_value;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);			
}

function control_update()
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{if (xmlhttp.readyState==4) 
		{
			if (xmlhttp.responseText.substring(0,1) == '[')
			{
				sensor_data = eval(xmlhttp.responseText);
				for (sensor_key in sensor_data)
				{
					sensor = sensor_data[sensor_key];
					sens_id = sensor[0];
					if (document.getElementById('s'+sens_id).hasFocus != true)
					{
						document.getElementById('s'+sens_id).value = sensor[1];
						document.getElementById('ss'+sens_id).innerHTML = sensor[2].substring(11);
					}
				}
			}
		}
	}
	var url="/device/sensors/control/ajax/?method=read";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);			
	
}