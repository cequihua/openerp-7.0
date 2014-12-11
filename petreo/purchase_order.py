from openerp.osv import osv, fields

class purchase_order(osv.Model):
	_inherit = 'purchase.order'

	_columns = {
		'centro_costo_id': fields.many2one('account.cost.center', 'Centro de Costos', ondelete="cascade", required=False, readonly=True), 
	}

	def create(self, cr, uid, vals, context=None):
		try:
			print vals
			warehouse_id = vals['warehouse_id']
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)#.centro_costo_id
			centro_costo_id = obj_warehouse['centro_costo_id']['id']
			vals['centro_costo_id'] = centro_costo_id
		except Exception, e:
			print e
		finally:
			return super(purchase_order, self).create(cr, uid, vals, context=context)

	def write(self, cr, uid, ids, vals, context=None):
		try:
			print vals
			warehouse_id = vals['warehouse_id']
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)#.centro_costo_id
			centro_costo_id = obj_warehouse['centro_costo_id']['id']
			vals['centro_costo_id'] = centro_costo_id
		except Exception, e:
			print e
		finally:
			return super(purchase_order, self).write(cr, uid, ids, vals, context=context)