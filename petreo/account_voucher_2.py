from openerp.osv import osv, fields

class account_voucher(osv.Model):
	_inherit = 'account.voucher'

	def create(self, cr, uid, vals, context=None):
		super(account_voucher, self).create(cr, uid, vals, context=context)
		print 'CREATE VOUCHER'
		print vals
		return True

	def write(self, cr, uid, ids, vals, context=None):
		super(account_voucher, self).write(cr, uid, ids, vals, context=context)
		print 'WRITE VOUCHER'
		print vals
		return True

	def button_proforma_voucher(self, cr, uid, ids, context=None):
		super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)
		print 'BUTTON VOUCHER'
		return True