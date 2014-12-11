from openerp.osv import osv, fields

class mrp_production(osv.Model):
	_inherit = 'mrp.production'

	_columns = {
		'pista':fields.char(string='Pista'),
	}

	def force_production(self, cr, uid, ids, *args):
		super(mrp_production, self).force_production(cr, uid, ids, *args)
		try:
			name_mrp_production = None
			centro_costo_id = None
			location_id = None
			account_move_line_ids = None

			obj_rmp_production = self.pool.get('mrp.production').read(cr, uid, ids)
			#print obj_rmp_production
			name_mrp_production = obj_rmp_production[0]['name']
			#print name_mrp_production
			location_id = obj_rmp_production[0]['location_src_id'][0]
			#print name_mrp_production
			#print location_id
			warehouse_ids = self.pool.get('stock.warehouse').search(cr, uid, [('lot_stock_id', '=', location_id)])
			#print warehouse_ids
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_ids)
			centro_costo_id = obj_warehouse[0]['centro_costo_id']['id']
			account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('name', '=', name_mrp_production)])
			#print account_move_line_ids
			self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})
			
		except Exception, e:
			print 'ERROR MRP force_production ' + str(e)
		finally:
			return True

class mrp_product_produce(osv.Model):
	_inherit = 'mrp.product.produce'

	def do_produce(self, cr, uid, ids, context=None):
		super(mrp_product_produce, self).do_produce(cr, uid, ids, context=context)
		try:
			name_mrp_production = None
			centro_costo_id = None
			location_id = None
			account_move_line_ids = None
			production_id = context.get('active_id', False)

			#print production_id
			obj_rmp_production = self.pool.get('mrp.production').read(cr, uid, production_id)
			#print obj_rmp_production
			name_mrp_production = obj_rmp_production['name']
			location_id = obj_rmp_production['location_src_id'][0]
			#print location_id
			warehouse_ids = self.pool.get('stock.warehouse').search(cr, uid, [('lot_input_id', '=', location_id)])
			#print warehouse_ids
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_ids)
			centro_costo_id = obj_warehouse[0]['centro_costo_id']['id']
			account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('name', '=', name_mrp_production)])
			#print account_move_line_ids
			if account_move_line_ids:
				self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})
				#print 'CENTRO DE COSTO AGREGADO'
		except Exception, e:
			print 'ERROR MRP PRODUCE do_produce ' + str(e)
		finally:
			return True

class stock_move_consume(osv.Model):
	_inherit = 'stock.move.consume'

	def do_move_consume(self,cr,uid,ids,context=None):
		super(stock_move_consume, self).do_move_consume(cr, uid, ids,context=context)
		try:
			name_move_line = ''
			stock_move_id = context.get('active_id', False)
			stock_move = self.pool.get('stock.move').read(cr,uid,stock_move_id)
			location_id = stock_move['location_id'][0]
			name_move_line = stock_move['name']
			#print location_id
			warehouse_id = self.pool.get('stock.warehouse').search(cr, uid, [('lot_input_id', '=', location_id)])
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)
			#print obj_warehouse
			centro_costo_id = obj_warehouse[0]['centro_costo_id']['id']
			account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('name', '=', name_move_line)])
			#print account_move_line_ids
			self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})
			#print 'STOCK CONSUME'
			#print stock_move['name']
		except Exception, e:
			print 'ERROR do_move_consume '  + str(e)
		finally:
			return True