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
			<td rowspan="6" scope="col">
				<table>
					<tr>
						<td>
							<center>
							${helper.embed_image('jpeg',str(o.res_company_id.logo),180, 85)}
							<center>
						</td>
						<td>
							<center>
							<h4>${o.res_company_id.name}</h4>
								${o.res_company_id.street} <br/>
								${o.res_company_id.city}  ${o.res_company_id.state_id.name} <br/>
								Tel. ${o.res_company_id.phone}  RFC: ${o.res_company_id.company_registry or ''|entity}
							</center>
						</td>
					</tr>
				</table>
			</td>
			</tr>
			<tr>
				<th colspan="4" scope="col" rowspan="1" class="titulo">REMISION</th>
			<tr>
			<tr>
				<td colspan="4" scope="col" rowspan="1" class="center"><h4>${o.name or ''|entity}</h4></td>
			</tr>
			<tr>
					<td class="titulo" class="center">FECHA</td>
					<td class="titulo" class="center">PLANTA</td>
					<td class="titulo" class="center">OBRA</td>
					<td class="titulo" class="center">CIUDAD</td>
			</tr>
			<tr>
					<td class="center"> 
						${o.create_date_document or ''|entity}
					</td>
					<td class="center">
					% if o.move_lines[0].location_id.partner_id:
						${o.move_lines[0].location_id.partner_id.name or ''|entity}
					% endif
					</td>
					<td>
					% if o.move_lines[0].location_dest_id.partner_id:
						${o.move_lines[0].location_dest_id.partner_id.name or ''|entity}
					% endif
					</td>
					<td class="center">
					% if o.move_lines[0].location_dest_id.partner_id:
						${o.move_lines[0].location_dest_id.partner_id.city or ''|entity}, ${o.move_lines[0].location_dest_id.partner_id.state_id.name or ''|entity}
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
				UNIDAD
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
			</td>
		</tr>
		% endfor
	</table>
	<br/>
	<table border="1px">
		<table border="1px">
		<tr>
			<td class="titulo" colspan="5">LOZA ALVEOLAR</td>
			<td></td>
			<td class="titulo" colspan="3"></td>
		</tr>
		<tr>
			<td class="titulo">CUADRANTE</td>
			<td class="titulo">ML. PIEZA</td>
			<td class="titulo">M2 PIEZA</td>
			<td class="titulo">No. PIEZA</td>
			<td class="titulo">SECCION</td>
			<td>&nbsp;</td>
			<td class="titulo">ml</td>
			<td class="titulo">m2</td>
			<td class="titulo">KG</td>
		</tr>
		<tr style="text-align:center">
		% for lin in o.move_lines:
			<td>${lin.cuadrante or ''|entity}</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		% endfor
		</tr>
		<tr>
			<td colspan="9">&nbsp;</td>
		</tr>
		<tr>
			<td class="titulo-left"><b>POLINES S:</b></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td style="text-align:right"><b>TOTAL:</b></td>
			<td><center></center></td>
			<td><center></center></td>
			<td><center></center></td>
		</tr>
		<tr>
			<td class="titulo-left"><b>POLINES E:</b></td>
			<td></td>
		</tr>
	</table>
	<br/>
	<table border="1px">
		<tr>
			<td colspan="1" class="titulo">HORARIOS DEL CR</td>
			<td colspan="2" class="titulo">ENTREGO:</td>
		</tr>
		<tr>
			<td><b>SALIDA DE PLANTA:</b></td>
			<td><b>DESPACHADOR:</b> ${o.despachador_id.name or ''|entity}</td>
			<td><b>ALMACEN PLANTA:</b> 
			% if o.move_lines[0].location_dest_id.partner_id:
			${o.move_lines[0].location_dest_id.partner_id.name or ''|entity}
			% endif
			</td>
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
	<br/>
	<table border="1px">
		<tr>
			<td colspan="1" class="titulo">RECIBIO EN OBRA:</td>
		</tr>
		<tr>
			<td><b>NOMBRE:</b></td>
		</tr>
		<tr>
			<td><b>PUESTO:</b></td>
		</tr>
		<tr>
			<td style="height:35px"><b>FIRMA:</b></td>
		</tr>
	</table>
	</body>
% endfor
</html>


<!-- ## -*- coding: utf-8 -*-
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
			.titulo-left{
				background-color: #E6E6E6;
				font-weight: bold;
				text-align: left;
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
			<td rowspan="5" scope="col">
				<center>
					${helper.embed_image('jpeg',str(o.res_company_id.logo),180, 85)}
				</center>
			</td>
			<td rowspan="5" scope="col">
				<center>
				<h4>${o.res_company_id.name}</h4>
				${o.res_company_id.street} <br/>
				${o.res_company_id.city}  ${o.res_company_id.state_id.name} <br/>
				Tel. ${o.res_company_id.phone}  RFC: ${o.res_company_id.company_registry or ''|entity}
				</center>
			</td>
		</tr>
		<tr>
			<td class="titulo-left">FOLIO:</td>
			<td><center><h4>${o.name or ''|entity}</h4></center></td>
		</tr>
		<tr>
			<td class="titulo-left">FECHA:</td>
			<td>${o.create_date_document or ''|entity}</td>
		</tr>
		<tr>
			<td class="titulo-left">OBRA:</td>
			<td>${o.move_lines[0].location_dest_id.partner_id.name or ''|entity}</td>
		</tr>
		<tr>
			<td class="titulo-left">FLETE:</td>
			<td>${o.unidad_id.name or ''|entity}</td>
		</tr>
		<tr>
			<td colspan="4" class="titulo">
				PRODUCTOS
			</td>
		</tr>
		% for lin in o.move_lines:
		<tr>
			<td class="center" colspan="4">
				${lin.product_id.name}
			</td>
		</tr>
		% endfor
	</table>

	<table border="1px">
		<tr>
			<td class="titulo" colspan="5">LOZA ALVEOLAR</td>
			<td></td>
			<td class="titulo" colspan="3"></td>
		</tr>
		<tr>
			<td class="titulo">CUADRANTE</td>
			<td class="titulo">ML. PIEZA</td>
			<td class="titulo">M2 PIEZA</td>
			<td class="titulo">No. PIEZA</td>
			<td class="titulo">SECCION</td>
			<td>&nbsp;</td>
			<td class="titulo">ml</td>
			<td class="titulo">m2</td>
			<td class="titulo">KG</td>
		</tr>
		<tr style="text-align:center">
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td colspan="9">&nbsp;</td>
		</tr>
		<tr>
			<td class="titulo-left">POLINES S:</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td class="titulo-left">TOTAL:</td>
			<td><center></center></td>
			<td><center></center></td>
			<td><center></center></td>
		</tr>
		<tr>
			<td class="titulo-left">POLINES E:</td>
			<td></td>
		</tr>
	</table>
	<table border="1px">
		<tr>
			<td><b>H. SALIDA PLANTA:</b></td>
			<td><b>H. ENTREGA A OBRA:</b></td>
			<td><b>H. DESCARGA OBRA:</b></td>
		</tr>
		<tr>
			<td><b>ALMACEN PLANTA:</b></td>
			<td><b>FLETE:</b></td>
			<td><b>RECIBIO EN OBRA:</b></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td style="height:35px"><b>FIRMA:</b></td>
		</tr>
	</table>
	% endfor
	</body>
</html> -->