from openerp.osv import osv, fields

class account_voucher(osv.Model):
	_inherit = 'account.voucher'

	def button_proforma_voucher(self, cr, uid, ids, context=None):
		super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)
		try:
			print 'BUTTON VOUCHER'
			obj_voucher = self.pool.get('account.voucher').read(cr, uid, ids)
			#print obj_voucher
			account_move_line_ids = obj_voucher[0]['move_ids']
			#move_line_ref = obj_voucher[0]['number']
			#move_line_ref2 = obj_voucher[0]['reference']
			#account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, ['|',('ref','=',move_line_ref.replace('/','')),('name','=',move_line_ref)])
			#account_move_line_ids = self.pool.get('account.move.line').search(cr, uid, [('ref','=',move_line_ref.replace('/',''))])

			obj_account_move_line_ids = self.pool.get('account.move.line').browse(cr, uid, account_move_line_ids)
			
			obj_invoice_ids = None
			obj_invoice = None

			for obj_line in obj_account_move_line_ids:
				obj_invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('number','=',obj_line['name'])])
				#print obj_invoice_ids
				if len(obj_invoice_ids) > 0:
					obj_invoice = self.pool.get('account.invoice').read(cr, uid, obj_invoice_ids)
				
			centro_costo_id = obj_invoice[0]['centro_costo_id'][0]
			self.pool.get('account.move.line').write(cr,uid,account_move_line_ids, {'centro_costo_id':centro_costo_id})

			print 'CENTRO DE COSTO AGREGADO'
		except Exception, e:
			print 'ERROR ' + str(e)
		finally:
			return True

	# def create(self, cr, uid, vals, context=None):
	# 	super(account_voucher, self).create(cr, uid, vals, context=context)
	# 	print 'CREATE VOUCHER'
	# 	print vals
	# 	return True

	# def write(self, cr, uid, ids, vals, context=None):
	# 	super(account_voucher, self).write(cr, uid, ids, vals, context=context)
	# 	print 'WRITE VOUCHER'
	# 	print vals
	# 	return True