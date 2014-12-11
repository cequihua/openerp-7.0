## -*- coding: utf-8 -*-
<%from datetime import date%>
<!DOCTYPE>
<html>
	<head>
		<title></title>
		<style type="text/css">
		${css}
			body{
				font-family: Arial Narrow;
			}

			table {
				font-size: 12px;
				width: 100%;
				border: 1px;
				border-width: 1px;
				border-collapse: collapse;
			}
			.titulo{
				background-color: #E6E6E6;
				font-weight: bold;
				text-align: center;
			}
			.center{
				text-align: center;
			}
		</style>
	</head>
	<body>
% for o in objects:
	<table border="1px">
		<tr>
			<td rowspan="4" scope="col">
				<center>
					<!-- <img src="data:image/png;base64,${o.res_company_id.logo}" alt="Red dot" /> -->
					${helper.embed_image('jpeg',str(o.res_company_id.logo),180, 85)}
				</center>
			</td>
			<td rowspan="4" scope="col">
				<center>
				<h4>${o.res_company_id.name}</h4>
				${o.res_company_id.street} <br/>
				${o.res_company_id.city}  ${o.res_company_id.state_id.name} <br/>
				Tel. ${o.res_company_id.phone}  RFC: ${o.res_company_id.company_registry or ''|entity}
				</center>
			</td>
			</tr>
			<tr>
				<th colspan="3" scope="col" class="titulo">REMISION</th>
			<tr>
			<tr>
				<td colspan="3" scope="col" class="center"><h4>${o.name or ''|entity}</h4></td>
			</tr>
			<tr>
				<th>
					<td class="titulo" class="center">FECHA</td>
					<td class="titulo" class="center">PLANTA</td>
					<td class="titulo" class="center">CIUDAD</td>
				</th>
			</tr>
			<tr>
				<th>
					<td class="center"> 
						${o.create_date_document or ''|entity}
					</td>
					<td class="center">
					% if o.move_lines[0].location_id.partner_id:
						${o.move_lines[0].location_id.partner_id.name or ''|entity}
					% endif
					</td>
					<td class="center">
					% if o.move_lines[0].location_dest_id.partner_id:
						${o.move_lines[0].location_dest_id.partner_id.city or ''|entity}, ${o.move_lines[0].location_dest_id.partner_id.state_id.name or ''|entity}
					% endif
					</td>
				</th>
			</tr>
			<tr>
				<td class="titulo">
					CLIENTE
				</td>
				<td class="titulo">
					FACTURAR A
				</td>
				<td class="titulo" colspan="3">
					OBRA
				</td>
			</tr>
			<tr>
				<td class="center">
				% if o.partner_id:
					<center>
					${o.partner_id.name or ''|entity} <br/>
					${o.partner_id.street or ''|entity} ${o.partner_id.street2 or ''|entity}<br/>
					${o.partner_id.city or ''|entity}, ${o.partner_id.state_id.name or ''|entity}, CP ${o.partner_id.zip or ''|entity}
					</center>
				% endif
				</td>
				<td class="center">
				% if o.partner_id:
					<center>
					${o.partner_id.name or ''|entity} <br/>
					${o.partner_id.street or ''|entity} <br/>
					${o.partner_id.city or ''|entity}, ${o.partner_id.state_id.name or ''|entity}, CP ${o.partner_id.zip or ''|entity}, RFC ${o.partner_id.vat or ''|entity}
					</center>
				% endif
				</td>
				<td class="center" colspan="3">
				% if o.move_lines[0].location_dest_id.partner_id:
					${o.move_lines[0].location_dest_id.partner_id.name or ''|entity}
				% endif
				</td>
			</tr>
	</table>
	<table border="1px">
		<tr class="titulo">
			<td>
				PRODUCTO
			</td>
			<td>
				CANTIDAD
			</td>
			<td>
				UNIDAD / TROMPO
			</td>
			<td>
				ESPECIFICACION
			</td>
		</tr>
		% for lin in o.move_lines:
		<tr class="center">
			<td>
				${lin.product_id.name}
			</td>
			<td>
				${lin.product_qty} ${lin.product_uom.name or ''|entity}
			</td>
			<td>
				${o.unidad_id.name or ''|entity}
			</td>
			<td>
				${lin.product_id.description or ''|entity}
				<br/>
				${o.note or ''|entity}
				<br/>
				<h4>ACUMULADO</h4>
				${lin.product_id.qty_available}
			</td>
		</tr>
		% endfor
	</table>
	<table border="1px">
		<tr>
			<td class="titulo">DATOS DEL COLADO</td>
		</tr>
		<tr>
			<td>
				<b>HORARIO DE INICIO:</b>
			</td>
		</tr>
		<tr>
			<td>
				<b>HORARIO DE FIN:</b>
			</td>
		</tr>
		<tr>
			<td>
				<b>HORA MUESTRA:</b>
			</td>
		</tr>
	</table>
	<table border="1px">
		<tr>
			<td colspan="1" class="titulo">HORARIOS DEL CR</td>
			<td colspan="2" class="titulo">ENTREGO:</td>
		</tr>
		<tr>
			<td><b>SALIDA DE PLANTA:</b></td>
			<td><b>DESPACHADOR:</b> ${o.despachador_id.name or ''|entity}</td>
			<td></td>
		</tr>
		<tr>
			<td><b>ENTREGA EN OBRA:</b></td>
			<td><b>UNIDAD:</b> ${o.unidad_id.name or ''|entity}</td>
			<td><b>PLACAS:</b> ${o.unidad_id.street or ''|entity}</td>
		</tr>
		<tr>
			<td></td>
			<td><b>BOMBA:</b> ${o.bomba_id.name or ''|entity}</td>
			<td><b>PLACAS:</b> ${o.bomba_id.street or ''|entity}</td>
		</tr>
		<tr>
			<td><b>LLEGADA A PLANTA:</b></td>
			<td><b>OPERADOR:</b> ${o.operador or ''|entity}</td>
			<td></td>
		</tr>
	</table>
	<table border="1px">
		<tr>
			<td colspan="2" class="titulo"></td>
			<td colspan="1" class="titulo">RECIBIO:</td>
		</tr>
		<tr>
			<td>HRS:</td>
			<td>HRS:</td>
			<td><b>NOMBRE:</b></td>
		</tr>
		<tr>
			<td>KM:</td>
			<td>KM:</td>
			<td><b>PUESTO:</b></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td style="height:35px"><b>FIRMA:</b></td>
		</tr>
	</table>
	</body>
% endfor
</html>