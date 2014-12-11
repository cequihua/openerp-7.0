from openerp.osv import osv, fields
class Sale(osv.Model):
	_inherit = 'sale.order'
	
	# def create(self, cr, uid, values, context=None):
 #    	values.update({'note': 'VALOR POR DEFAULT'})
 #    	res = super('create',self).create(cr,uid,values,context=context)
 #        return res