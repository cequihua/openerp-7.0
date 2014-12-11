import pdb
from openerp.osv import osv, fields

class stock_partial_picking(osv.Model):
	_inherit = 'stock.partial.picking'

	def do_partial(self, cr, uid, ids, context=None):
		super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)
		try:
			#pdb.set_trace()
			purchase_id = 0
			sale_id = 0
			centro_costo_id = 0
			account_move_line_ids = None
			account_move_ref = ''
			account_move_ref2 = ''
			#backorder_id = 0

			obj_stock_partial_picking = self.pool.get('stock.partial.picking').read(cr, uid, ids)
			#print obj_stock_partial_picking
			stock_picking_id = obj_stock_partial_picking[0]['picking_id'][0]
			obj_stock_picking = self.pool.get('stock.picking').read(cr, uid, [stock_picking_id])
			#print obj_stock_picking
			account_move_ref = obj_stock_picking[0]['name']
			if obj_stock_picking[0]['backorder_id']:
				account_move_ref2 =  obj_stock_picking[0]['backorder_id'][1]
			#print obj_stock_picking
			if obj_stock_picking[0]['purchase_id']:
				purchase_id = obj_stock_picking[0]['purchase_id'][0]
				obj_purchase_order =  self.pool.get('purchase.order').read(cr, uid, [purchase_id])
				centro_costo_id = obj_purchase_order[0]['centro_costo_id'][0]
			elif obj_stock_picking[0]['sale_id']:
				sale_id = obj_stock_picking[0]['sale_id'][0]
				obj_sale_order =  self.pool.get('sale.order').read(cr, uid, [sale_id])
				centro_costo_id = obj_sale_order[0]['centro_costo_id'][0]

			account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('ref','=',account_move_ref)])
			if account_move_line_ids:
				self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})
				print 'Centro costo agregado a ' + str(account_move_ref)
			else:
				account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('ref','=',account_move_ref2)])
				self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})
				print 'Centro costo agregado a ' + str(account_move_ref2)
			
			#print account_move_ref
		except Exception, e:
			print str(e)
		finally:
			return True

# class stock_pickinng_in(osv.Model):
# 	_inherit = 'stock.picking.in'

# 	def action_process(self, cr, uid, ids, context=None):
# 		return super(stock_pickinng_in, self).action_process(cr, uid, ids, context=context)
		