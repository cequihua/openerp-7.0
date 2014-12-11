#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class stock_move(osv.Model):
	_inherit = 'stock.move'

	_columns = {
		'cuadrante': fields.char(string='Cuadrante'),
	}
