<head><title>Data From Drivers</title>
<style type="text/css">

p.know{background-color: green;}

</style>



</head>
<body>
<a href="/">Home</a>
	<a href="/drivers">Corredores</a>
	<a href="/starttimes">Tiempos de Largada</a>
	<a href="/stage">Etapas</a>
	<a href="/resultado">Resultados</a>


<h1>Data from Drivers in Stage 1</h1>
<table border="1">
	<thead>
		<tr>
			<th bgcolor="gray"> Vehicle </th>
			<th bgcolor="gray"> Start Time </th>
			<th bgcolor="gray"> Time Arrive K30 </th>
			<th bgcolor="gray"> Result K30 </th>
			<th bgcolor="gray"> Time Arrive K54 </th>
			<th bgcolor="gray"> Result K54 </th>
			<th bgcolor="gray"> Time Arrive K112 </th>
			<th bgcolor="gray"> Result K112 </th>
			<th bgcolor="gray"> Time Arrive CP1 </th>
			<th bgcolor="gray"> Result CP1 </th>
			<th bgcolor="gray"> Time Arrive DZ186 </th>
			<th bgcolor="gray"> Result DZ186 </th>
			<th bgcolor="gray"> Time Arrive K230 </th>
			<th bgcolor="gray"> Result K230 </th>
			<th bgcolor="gray"> Time Arrive ASS1 </th>
			<th bgcolor="gray"> Result ASS1 </th>
		</tr>
	</thead>
<tbody>
	% for item in data:
	<tr>
       <td>{{item['vehicle']}}</td>
       <td>{{item['startt']}}</td>
       <td>{{item['timeK30']}}</td>
       <td>{{item['K30']}}</td>
       <td>{{item['timeK54']}}</td>
       <td>{{item['K54']}}</td>
       <td>{{item['timeK112']}}</td>
       <td>{{item['K112']}}</td>
       <td>{{item['timeCP1']}}</td>
       <td>{{item['CP1']}}</td>
       % if item['timeK112'] == 'Unknow':
  				<td>{{item['timeK112']}}</td>
		%else:
			  
			  <td><p class="know">{{item['timeK112']}}</p></td>
		% end
       
       <td>{{item['DZ186']}}</td>
       <td>{{item['timeK230']}}</td>
       <td>{{item['K230']}}</td>
       <td>{{item['timeASS1']}}</td>
       <td>{{item['ASS1']}}</td>
	   
	</tr>
	% end
</tbody>
</table>
</body>