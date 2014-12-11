#!/usr/bin/env python
# -*- encoding: utf-8 -*-

{
'name' : "PETREOMECANIC",
'category' : "Reports",
'version' : "1.0",
'depends' : ['base', 'account', 'purchase', 'sale', 'sfs_account_cost_center'],
'author' : "Tantums",
'description' : """\
Reporte de de compras reales""",
'data' : ['view/warehouse_view.xml', 'view/account_view.xml', 'view/account_view.xml', 
		'view/sale_order_view.xml', 'view/purchase_order_view.xml', 'view/stock_picking_view.xml', 
		'view/stock_move_view.xml', 'reports/remision_stock_picking_report.xml',
		'reports/remision_losa_stock_picking_report.xml', 'view/mrp_view.xml']
}