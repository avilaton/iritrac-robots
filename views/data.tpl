<head><title>Data From Drivers</title>
<style type="text/css">

	p.know{background-color: #04B404;}
	p.title {background-color: #088A68;}
	p.row {background-color: #A9F5BC;}
	.buttons a, .buttons button{
    display:inline;
    
    margin:0 7px 0 0;
    background-color:#f5f5f5;
    border:1px solid #dedede;
    border-top:1px solid #eee;
    border-left:1px solid #eee;

    font-family:"Lucida Grande", Tahoma, Arial, Verdana, sans-serif;
    font-size:12px;
    line-height:130%;
    text-decoration:none;
    font-weight:bold;
    color:#565656;
    cursor:pointer;
    padding:5px 10px 6px 7px; /* Links */
}
.buttons button{
    width:auto;
    overflow:visible;
    padding:4px 10px 3px 7px; /* IE6 */
}
.buttons button[type]{
    padding:5px 10px 5px 7px; /* Firefox */
    line-height:17px; /* Safari */
}
*:first-child+html button[type]{
    padding:4px 10px 3px 7px; /* IE7 */
}
.buttons button img, .buttons a img{
    margin:0 3px -3px 0 !important;
    padding:0;
    border:none;
    width:16px;
    height:16px;
}

/* STANDARD */

button:hover, .buttons a:hover{
    background-color:#dff4ff;
    border:1px solid #c2e1ef;
    color:#336699;
}
.buttons a:active{
    background-color:#6299c5;
    border:1px solid #6299c5;
    color:#fff;
}

/* POSITIVE */

button.positive, .buttons a.positive{
    color:#529214;
}
.buttons a.positive:hover, button.positive:hover{
    background-color:#E6EFC2;
    border:1px solid #C6D880;
    color:#529214;
}
.buttons a.positive:active{
    background-color:#529214;
    border:1px solid #529214;
    color:#fff;
}

/* NEGATIVE */

.buttons a.negative, button.negative{
    color:#d12f19;
}
.buttons a.negative:hover, button.negative:hover{
    background:#fbe3e4;
    border:1px solid #fbc2c4;
    color:#d12f19;
}
.buttons a.negative:active{
    background-color:#d12f19;
    border:1px solid #d12f19;
    color:#fff;
}

/* REGULAR */

button.regular, .buttons a.regular{
    color:#336699;
}
.buttons a.regular:hover, button.regular:hover{
    background-color:#dff4ff;
    border:1px solid #c2e1ef;
    color:#336699;
}
.buttons a.regular:active{
    background-color:#6299c5;
    border:1px solid #6299c5;
    color:#fff;
}

</style>
	%nametime = []
	%for i in timename:
		%nametime.append(i)
	%end
	%resulttime = []
	%for i in timeresult:
		%resulttime.append(i)
	%end

	%resultzone = []
	%for i in zoneresult:
		%resultzone.append(i)
	%end

	%vehicle = []
	%for i in vehiculo:
		%vehicle.append(i)
	%end

	%starttime = []
	%for i in startime:
		%starttime.append(i)
	%end
%col = 2 + (len(nametime))*2
</head>
<body bgcolor="#D8D8D8">

	<div class="buttons">
		<a href="/" class="regular">Home</a>
		<a href="/starttimes" class="regular">Tiempos de Largada</a>
		<a href="/stage" class="regular">Etapas</a>
		<a href="/resultado" class="regular">Resultados</a>
	</div>

	<div>
		<form action="/updaterep" method="post">
			<button type="submit">Update Data</button> <i>Last Update {{fecha}}</i>
		</form>
	
		<form action="/resultado" method="post">
			<i>Select Stage </i>
				<select name="stage">
			  		<option value="1">1</option>
			  		<option value="2">2</option>
			  		<option value="3">3</option>
			  		<option value="4">4</option>
				</select>
			<button type="submit">Select </button>
		</form>
	
	
		<form action="/" method="post">
			<i>Desde: </i> <input align="center" type="text" name="from" placeholder="YYYY-MM-DD">
			<i>Hasta: </i> <input type="text" name="to" placeholder="YYYY-MM-DD">
			<button type="submit" class="standar">Cargar</button>
		</form>
	</div>


<table border="1">
	<thead>
		<tr><th bgcolor="gray" colspan={{col}}><p class="title"> Stage Id Nº {{stage_id}} </th></tr>
		<tr>
			<th><p class="title"> Vehicle </th>
			<th><p class="title">Start Time</th>
			
			%for j in zonename:
			<th colspan="2"><p class="title"> Stage {{j}}</p></th>
			<!--<th bgcolor="gray">{{j}}</th>-->
			%end

		</tr>
	</thead>
<tbody>

	

	
	<tr>
		<td>#</td>
		<td>#</td>
		%for a in range(len(nametime)):
		<td>Arrive</td>
		<td>Dif</td>
		
		%end
	</tr>
	%for q in range(len(vehicle)):
	<tr>

			<td><p class="title">{{vehicle[q]}}</p></td>
			<td><p class="title">{{starttime[q]}}</p></td>
			%for k in range(len(nametime)):
				% t = (q*len(nametime))+ k
				%if resulttime[t] == ' ':
       				
       				<td>{{resulttime[t]}}</td>
  					<td>{{resultzone[t]}}</td>
  					
  				%else:
		
			  		<td><p class="know">{{resulttime[t]}}</p></td>
			  		<td><p class="know">{{resultzone[t]}}</p></td>
			  		

				% end
       		%end
       	%end

	</tr>
	
	
	
	
</tbody>
</table>
</body>