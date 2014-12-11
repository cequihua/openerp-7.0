## -*- coding: utf-8 -*-
<html>
<head>
	<style type="text/css">
		${css}
			body{
				font-family: System;
			}

			table {
				font-size: 10px;
				width: 100%;
				border:1px;
				border-width: 1px;
				border-collapse: collapse;
			}
			.titulo{
				background-color: #0B3861;
				font-weight: bold;
				color:white;
				text-align: center;
			}
			.titulo2{
				background-color: #0B3861;
				font-weight: bold;
				color:white;
				text-align: left;
			}
			.center{
				text-align: center;
			}
			.text_left{
				text-align: right;
			}
			.text_center{
				text-align: center;
				font-weight: bold;
			}
		</style>
</head>
<body>
%for o in get_loan(data):
	<table border="1px">
		<caption>ESTADO DE CUENTA MENSUAL</caption>
		<tr>
			<td rowspan="11" colspan="2" style="font-weight: bold;">
				${helper.embed_image('jpeg',str(o.partner_id.company_id.logo),180, 85)}
				<br/>
				<b>RFC:</b> AXR4535353<br/>
				<b>No. Cuenta:</b> 645454545454454<br/>
				<b>No. Cliente:</b> 324455<br/>
				Nombre: ${o.partner_id.name}<br/>
				Domicilio: ${o.partner_id.street}, ${o.partner_id.city}, ${o.partner_id.country_id.name}, CP: ${o.partner_id.zip}<br/>
			</td>
		</tr>
		<tr>
			<td colspan="2" class="titulo"><center>CREDITO</center></td>
		</tr>
		<tr>
			<td colspan="2"><center>${o.loan_id}</center></td>
		</tr>
		<tr>
			<td colspan="2" class="titulo"><center>FECHA</center></td>
		</tr>
		<tr>
			<td colspan="2"><center>${o.apply_date}</center></td>
		</tr>
		<tr>
			<td colspan="2">&nbsp;</td>
		</tr>
		%for p in get_loan_payment(data):
		<tr style="font-size: 16px; font-weight: bold;">
			<td>PAGO MENSUAL</td>
			<td style="text-align:right">${p.pago_mes + (p.interes * 0.16)}</td>
		</tr>
		<tr class="titulo2">
			<td>FECHA LIMITE DE PAGO</td>
			<td>${p.fecha}</td>
		</tr>
		<tr class="text_left">
			<td style="font-weight: bold;">CAPITAL</td>
			<td>${p.capital_mes}</td>
		</tr>
		<tr class="text_left">
			<td style="font-weight: bold;">INTERESES</td>
			<td>${p.interes}</td>
		</tr>
		<tr class="text_left">
			<td style="font-weight: bold;">IVA</td>
			<td>${p.interes * 0.16}</td>
		</tr>
		<tr>
			<td style="font-weight: bold;">MONTO</td>
			<td>${o.loan_amount}</td>
			<td class="text_left"></td>
			<td class="text_left"></td>
		</tr>
		<tr>
			<td style="font-weight: bold;">TASA INTERES MENSUAL</td>
			<td>${o.tasa_int_mensual}<td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td style="font-weight: bold;">CAT</td>
			<td>${o.cat}</td>
			<td class="titulo2">SALDO ACTUAL</td>
			<td class="titulo2" style="text-align:right">${p.capital + get_saldo_pen_total(data)}</td>
		</tr>
	</table>
	<br/>
	<table border="1px" summary="">
		<tr class="titulo">
			<td colspan="7"><center>RESUMEN DE LA CUENTA</center></td>
		</tr>
		<tr class="text_center">
			<td>FECHA</td>
			<td>CONCEPTO</td>
			<td>INTERES</td>
			<td>IVA</td>
			<td>CAPITAL</td>
			<td>PAGO MENSUAL</td>
			<td>SALDO ANTERIOR</td>
		</tr>
		% endfor
		%for pm in get_loan_payments(data):
		<tr style="text-align:center">
			<td>${pm.fecha}</td>
			<td>${pm.pago_mes + (pm.interes * 0.16)} SU PAGO GRACIAS</td>
			<td>${pm.interes}</td>
			<td>${pm.interes * 0.16}</td>
			<td>${pm.capital_mes}</td>
			<td>${pm.pago_mes + (pm.interes * 0.16)}</td>
			<td>${pm.capital}</td>
		</tr>
		% endfor
	</table>
% endfor
</body>L
</html>