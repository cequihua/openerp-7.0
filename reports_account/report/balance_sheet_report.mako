## -*- coding: utf-8 -*-
<html>
<head>
	<style type="text/css">
		${css}
			body{
				font-family: Helvetica-Oblique;
			}

			.table_acc {
				width: 100%;
				border:0px;
				border-collapse: collapse;
				font-size: 9px;
			}
			.header {
				font-weight: bold;
				font-size: 11px;
				width: 100%;
				text-align: center;
			}
		</style>
</head>
<body>

	<center>
	
		<table class="header">
			<tr>
				<td rowspan="5">${helper.embed_image('jpeg',str(get_company_logo(data['form'])),180, 85)}</td>
			</tr>
			<tr>
				<td>${data['form']['company_id'][1].upper()}</td>
			</tr>
	
			<tr>
				<td>${_('BALANCE GENERAL')}</td>
			</tr>
			<tr>
				<td>${_('Expresado en')} ${exchange_name(data['form'])}</td>
			</tr>
			<tr>
				<td>${get_month(data['form'])}</td>
			</tr>
		</table>
	</center>
	<br/>
	<table class="table_acc">
		<tr style="font-weight: bold;">
			<td>${_('CODIGO')}</td>
			<td>${_('CUENTA')}</td>
			<td>${_('ACUMULADO')} <br/>${_('PERIODO ANT.')}</td>
			<td>${_('ABONOS')}</td>
			<td>${_('CARGOS')}</td>
			<td>${_('SALDO DEL')} <br/>${_('PERIODO')}</td>
			<td>${_('SALDO')} <br/>${_('ACUMULADO')}</td>
		</tr>
		<tr>
			<td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td>
		</tr>
	%for o in lines(data['form']):
		%if o['id'] == 0:
		<tr>
			<td></td><td></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td><td><hr/></td>
		</tr>
		%endif
		<tr>
			%if o['type'] == 'view' or o['id'] == 0 and o['level'] != 1:
			<td style="font-weight: normal; font-size:9px;">${o['code']}</td>
			%else:
			<td>${o['code']}</td>
			%endif

			%if o['type'] == 'view' or o['id'] == 0 and o['level'] != 1:
			<td style="font-weight: normal; font-size:9px;">${o['name'].upper()}</td>
			%else:
			<td>${o['name']}</td>
			%endif
			
			%if o['level'] != 1:
			<td>${to_money(o['balanceinit'])}
			%elif o['id'] == 0:
			<td style="font-weight: normal; font-size:12px;">	${to_money(o['balanceinit'])}
			%endif
			
			%if o['level'] != 1:
			<td>${to_money(o['debit'])}</td>
			%elif o['id'] == 0:
			<td style="font-weight: normal; font-size:12px;">	${to_money(o['debit'])}</td>
			%endif
			
			%if o['level'] != 1:
			<td>${to_money(o['credit'])}</td>
			%elif o['id'] == 0:
			<td style="font-weight: normal; font-size:12px;">	${to_money(o['credit'])}</td>
			%endif
			
			%if o['level'] != 1:
			<td>${to_money(o['ytd'])}</td>
			%elif o['id'] == 0:
			<td style="font-weight: normal; font-size:12px;">	${to_money(o['ytd'])}</td>
			%endif
			
			%if o['level'] != 1:
			<td>${to_money(o['balance'])}</td>
			%elif o['id'] == 0:
			<td style="font-weight: normal; font-size:12px;">	${to_money(o['balance'])}</td>
			%endif
			
		</tr>
		%if o['id'] == 0:
		<tr>
			<td><br/></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
		</tr>
		%endif
	%endfor
	</table>
</body>
</html>