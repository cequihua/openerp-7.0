from openerp.osv import osv, fields

class almacen(osv.Model):
	_inherit = 'stock.warehouse'

	_columns = {
		'centro_costo_id': fields.many2one('account.cost.center', 'Centro de Costos', ondelete="cascade", required=False), 
	}