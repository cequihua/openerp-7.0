<html>
% for order in objects:
	<head>
		<style type="text/css">
		${css}

		#content{
			font-family: Arial;font-size: 12px;height: 800px;
		}

		#header{
			float: right;
		}

		#detail-header{
			text-align: left;
		}

		#footer{
			height: 100px;text-align: right;float: right; clear: both;
		}

		#texto{
			text-align: left;width: 600px;float: left;
		}
		#detail-lines{
			width: 100%;
		}
		#table-detail-lines{
			width: 100%;border-color: black;text-align: right;
		}
		#detail-total{
			float: right;width: 100%;
		}
		#table-detail-total{
			border-color: black;text-align: right;float: right;
		}

		#table-detal-info{
			width: 100%;text-align: left;
		}
		.bold{
			font-weight: bold;
		}
		hr{
			background-color: #DF7401;
		}
		table{
			border-collapse: collapse; 
		}
		</style>
		<div id="header" style="width:100%">
		<table width="100%">
			<tr>
				<td><img src="data:image/png;base64,${order.company_id.logo}" alt="Red dot" /></td>
			</tr>
		</table>
		<hr/>
		</div>
	</head>
	<body>
	<div id="content">
		<div id="detail-header">
				<table id="table-detal-info">
					<tr>
						<td class="bold">
							Cotización:
						</td>
						<td>
							${order.name}
						</td>
						<td>
							
						</td>
						<td class="bold">
							Fecha:
						</td>
						<td>
							${order.date_order}
						</td>
					</tr>
					<tr>
						<td class="bold">
							Nombre:
						</td>
						<td>
							${order.partner_id.parent_id.name}
						</td>
					</tr>
					<tr>
						<td class="bold">
							Atención:
						</td>
						<td>
							${order.partner_id.name}
						</td>
					</tr>
					<tr>
						<td class="bold">
							Dirección:
						</td>
						<td>
							${order.partner_id.street}, ${order.partner_id.city}, CP. ${order.partner_id.zip}, ${order.partner_id.state_id.name}, ${order.partner_id.country_id.name}
						</td>
					</tr>
				</table>
				<br/>
				<br/>
			<div id="detail-lines">
			<div style="color:#DF7401; font-weight: bold; text-align:center; font-size:14px;">COTIZACION</div>
				<table id="table-detail-lines" border="1">
					<thead style="background-color: gray; color:white;">
						<th><center>CANTIDAD</center></th>
						<th><center>DESCRIPCION</center></th>
						<th><center>PARTE</center></th>
						<th><center>PRECIO</center></th>
						<th><center>IMPORTE</center></th>
					</thead>
					<tbody>
						% for lin in order.order_line:
							<tr>
								<td>${lin.product_uom_qty}</td>
								<td>${lin.product_id.name}</td>
								<td>${lin.product_id.default_code}</td>
								<td>$ ${lin.price_unit}</td>
								<td>$ ${lin.price_subtotal}</td>
							</tr>
						% endfor
					</tbody>
				</table>
			</div>
			<div id="detail-total">
				<table id="table-detail-total" border="1">
					<tr>
						<td class="bold">SUBTOTAL</td>
						<td>$ ${order.amount_untaxed}</td>
					<tr>
						<td class="bold">IVA</td>
						<td>$ ${order.amount_tax}</td>
					</tr>
					<tr>
						<td style="color: #DF7401;"  class="bold">TOTAL</td>
						<td style="color: #DF7401;"  class="bold">$ ${order.amount_total}</td>
					</tr>
					</tr>
				</table>
			</div>
			<div id="texto">
				${order.note}
			</div>
		</div>
		<div id="footer">
			<table>
				<tr>
					<td>
						${order.company_id.street}, ${order.company_id.street2}
					</td>
				</tr>
				<tr>
					<td>
						Tel. ${order.company_id.phone}
					</td>
				</tr>
				<tr>
					<td>
						Correo: ${order.company_id.email}
					</td>
				</tr>
			</table>
		</div>
	</div>
	</div>
	</body>
	% endfor
</html>