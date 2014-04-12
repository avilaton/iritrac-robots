<h1>Vehicle {{alpha}} times</h1>
<table>
	<thead>
		<tr>
			<th>Alpha</th>
			<th>DATE</th>
		</tr>
	</thead>
<tbody>
	% for item in lista:
	<tr>
	    <td>{{item['Alpha']}}</td>
	    <td>{{item['DATE']}}</td>
	</tr>
	% end
</tbody>
</table>