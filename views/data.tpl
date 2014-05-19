<h1>Vehicle {{driver_id}} data</h1>
<table>
	<thead>
		<tr>
			<th>Alpha</th>
			<th>DATE</th>
		</tr>
	</thead>
<tbody>
	% for item in data:
	<tr>
	    <td>{{item.id}}</td>
	    <td>{{item.alpha}}</td>
	</tr>
	% end
</tbody>
</table>