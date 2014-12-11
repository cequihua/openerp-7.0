#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
#from datetime import datetime, timedelta
#from pytz import timezone
import pytz
import time
import datetime

class stock_picking_in(osv.Model):
	_inherit = 'stock.picking.in'

	_columns = {
		'remision': fields.char(string="Remision"),
	}
	# def create(self, cr, uid, vals, context=None):
	# 	print vals
	# 	return super(stock_picking_in, self).create(cr, uid, vals, context=context)

	# def write(self, cr, uid, ids, vals, context=None):
	# 	#print vals
	# 	return super(stock_picking_in, self).write(cr, uid, ids, vals, context=context)

class stock_picking(osv.Model):
	_inherit = 'stock.picking'

	def _get_time_zone(self, cr, uid, context=None):
		if context is None:
			context = {}
		res_users_obj = self.pool.get('res.users')
		userstz = res_users_obj.browse(cr, uid, [uid])[0].partner_id.tz
		a = 0
		if userstz:
			hours = timezone(userstz)
			fmt = '%Y-%m-%d %H:%M:%S %Z%z'
			now = datetime.now()
			loc_dt = hours.localize(datetime(now.year, now.month, now.day,now.hour, now.minute, now.second))
			timezone_loc = (loc_dt.strftime(fmt))
			diff_timezone_original = timezone_loc[-5:-2]
			timezone_original = int(diff_timezone_original)
			s = str(datetime.now(pytz.timezone(userstz)))
			s = s[-6:-3]
			timezone_present = int(s)*-1
			a = timezone_original + ((
				timezone_present + timezone_original)*-1)
			return a

	def _get_create_date(self, cr, uid,context=None):
		#htz = self._get_time_zone(cr, uid, context=context)
		#fecha = fecha and datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') + timedelta(hours=htz) or False
		
		#fecha = datetime.now()
		#fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S') + timedelta(hours=htz)
		fmt = '%Y-%m-%d %H:%M'
		#date = self.default_get(cr,uid,['name','date'])['date']
		#date_object = datetime.strptime(date, fmt)
		#d1 = date_object(pytz.timezone("America/Monterrey"))
		#print d1
		d = datetime.datetime.now(pytz.timezone("America/Monterrey"))
		# print d
		d_string = d.strftime(fmt)
		fecha = datetime.datetime.strptime(d_string, fmt)
		# print d_string 
		# print d2.strftime(fmt)
		return fecha

	_columns = {
		'res_company_id': fields.many2one('res.company', string="Company", ondelete="cascade"),
		'despachador_id': fields.many2one('res.users', string="Despachador", ondelete="cascade"),
		'unidad_id': fields.many2one('res.partner', string="Unidad", ondelete="cascade", domain=[('supplier','=',False),('customer','=',False)]),
		'bomba_id': fields.many2one('res.partner', string="Bomba", ondelete="cascade", domain=[('supplier','=',False),('customer','=',False)]),
		'operador': fields.char(string="Operador"),
		'create_date_document': fields.datetime('Fecha de Creacion del documento'),
		'remision': fields.char(string="Remision"),
	}

	_defaults = {
		'res_company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'stock.picking', context=c),
		'despachador_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).id,
		'create_date_document': _get_create_date,
		#'date': _get_create_date,
		#lambda self, cr, uid, context=None: uid,
		#'create_date_document': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
	}
	# def action_process(self, cr, uid, ids, context=None):
	# 	return super(stock_picking, self).action_process(cr, uid, ids, context=context)