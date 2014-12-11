from openerp.osv import osv, fields

class account_voucher(osv.Model):
	_inherit = 'account.voucher'

	def create(self, cr, uid, vals, context=None):
		super(account_voucher, self).create(cr, uid, vals, context=context)
		try:
			#shop_id = vals['shop_id']
			#account_move_ids = self.pool.get('sale.shop').search(cr, uid, [('shop_id','=',shop_id)])
			print 'CREATE VOUCHER'
			print vals
		except Exception, e:
			print e
		finally:
			return True

	def write(self, cr, uid, ids, vals, context=None):
		super(account_voucher, self).write(cr, uid, ids, vals, context=context)
		try:
			print 'WRITE VOUCHER'
			print vals
			#move_id = vals['move_id']
			#obj_account_move_line = self.pool.get('account.move.line').read(cr, uid, [move_id])
			#print obj_account_move_line

			#invoice_id = vals['invoice'][0]
			#obj_invoice = self.pool.get('account.invoice').browse(cr, uid, [invoice_id])
			#print obj_invoice
			
		except Exception, e:
			print e
		finally:
			return True

	def button_proforma_voucher(self, cr, uid, ids, context=None):
		super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)
		try:
			print 'BUTTON PAGAR '
			#obj_pago = self.pool.get('account.voucher').read(cr,uid,ids)
			#print obj_pago
			#print obj_pago[0]['move_ids']
		except Exception, e:
			print e
		finally:
			return True