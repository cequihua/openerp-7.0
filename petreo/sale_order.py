from openerp.osv import osv, fields

class sale_order(osv.Model):
	_inherit = 'sale.order'

	_columns = {
		'centro_costo_id': fields.many2one('account.cost.center', 'Centro de Costos', ondelete="cascade", required=False, readonly=True), 
	}

	def create(self, cr, uid, vals, context=None):
		try:
			print vals
			shop_id = vals['shop_id']
			obj_sale_shop = self.pool.get('sale.shop').read(cr, uid, [shop_id])
			#print obj_sale_shop
			warehouse_id = obj_sale_shop[0]['warehouse_id'][0]
			#print warehouse_id
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)#.centro_costo_id
			centro_costo_id = obj_warehouse['centro_costo_id']['id']
			vals['centro_costo_id'] = centro_costo_id
		except Exception, e:
			print e
		finally:
			return super(sale_order, self).create(cr, uid, vals, context=context)

	def write(self, cr, uid, ids, vals, context=None):
		try:
			print vals
			shop_id = vals['shop_id']
			obj_sale_shop = self.pool.get('sale.shop').read(cr, uid, [shop_id])
			#print obj_sale_shop
			warehouse_id = obj_sale_shop[0]['warehouse_id'][0]
			#print warehouse_id
			obj_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)#.centro_costo_id
			centro_costo_id = obj_warehouse['centro_costo_id']['id']
			vals['centro_costo_id'] = centro_costo_id
		except Exception, e:
			print e
		finally:
			return super(sale_order, self).write(cr, uid, ids, vals, context=context)
