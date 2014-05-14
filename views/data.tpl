<h1>Vehicle {{alpha}} times</h1>
<form enctype="multipart/form-data" action="/data" method="post">
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
	% for item in lista:
	<tr>
	    <td>{{item.store['Alpha']}}</td>
	    <td>{{item.store['DATE']}}</td>
	</tr>
	% end
</tbody>
</table>