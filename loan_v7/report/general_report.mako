## -*- coding: utf-8 -*-
<html>
<head>
	<style type="text/css">
		${css}
			body{
				font-family: Arial Narrow;
			}

			table {
				font-size: 12px;
				width: 100%;
				border:1px;
				border-width: 1px;
				border-collapse: collapse;
			}
			.titulo{
				background-color: #084B8A;
				font-weight: bold;
				color:white;
				text-align: center;
				font-size: 14px;
			}
			.titulo2{
				background-color: black;
				font-weight: bold;
				color:white;
				text-align: left;
			}
			.center{
				text-align: center;
			}
			.text_left{
				text-align: right;
				font-weight: bold;
			}
			.text_center{
				text-align: center;
				font-weight: bold;
			}
		</style>
</head>
<body>
	<table border="1px">
		<tr>
			<td colspan="5" class="titulo">CREDITO DEL CLIENTE</td>
			<td colspan="4" class="titulo">ORIGEN DEL CREDITO</td>
		</tr>
		<tr>
			<td class="titulo">CLIENTE</td>
			<td class="titulo">CREDITO</td>
			<td class="titulo">MONTO</td>
			<td class="titulo">ABONO</td>
			<td class="titulo">SALDO</td>
			<td class="titulo">PROVEEDOR</td>
			<td class="titulo">MONTO</td>
			<td class="titulo">ABONO</td>
			<td class="titulo">SALDO</td>
		</tr>
	%for o in get_report_general(data):
		<tr>
			<td class="text_center">${o['cliente']}</td>
			<td class="text_center">${o['credito']}</td>
			<td class="text_left">${o['monto_cli']}</td>
			<td class="text_left">${o['abono_cli']}</td>
			<td class="text_left">${o['saldo_cli']}</td>
			<td class="text_center">${o['proveedor']}</td>
			<td class="text_left">${o['monto_pro']}</td>
			<td class="text_left">${o['abono_pro']}</td>
			<td class="text_left">${o['saldo_pro']}</td>
		</tr>
	% endfor
	</table>
</body>
</html>