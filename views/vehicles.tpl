<h1>Vehicles</h1>
<form enctype="multipart/form-data" action="/vehicles" method="post">
<p>File: <input type="file" name="file"></p>
<p><input type="submit" value="Upload"></p>
</form>
<table>
	<thead>
		<tr>
			<th>Alpha</th>
			<th>DATE</th>
		</tr>
	</thead>
<tbody>
	% for item in vehicles:
	<tr>
	    <td>{{item}}</td>
	    <td>{{item}}</td>
	</tr>
	% end
</tbody>
</table>