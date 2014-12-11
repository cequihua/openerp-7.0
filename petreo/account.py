from openerp.osv import osv, fields

class account_invoice(osv.Model):
	_inherit = 'account.invoice'

	_columns = {
		'centro_costo_id': fields.many2one('account.cost.center', 'Centro de Costos', ondelete="cascade", required=True), 
	}

	def invoice_validate(self, cr, uid, ids, context=None):
		try:
			print 'INVOICE VALIDATE'
			obj_invoice = self.pool.get('account.invoice').read(cr,uid,ids)
			centro_costo_id = obj_invoice[0]['centro_costo_id'][0]
			move_id = obj_invoice[0]['move_id'][0]
			account_move_ids = self.pool.get('account.move.line').search(cr, uid, [('move_id','=',move_id)])
			obj_account_move_line = self.pool.get('account.move.line').read(cr, uid, account_move_ids)
			self.pool.get('account.move.line').write(cr,uid,account_move_ids, {'centro_costo_id':centro_costo_id})
		except Exception, e:
			print 'ERROR ' + str(e)
		finally:
			return super(account_invoice,self).invoice_validate(cr, uid, ids, context=context)

	# def invoice_pay_customer(self, cr, uid, ids, context=None):
	# 	return super(account_invoice,self).invoice_pay_customer(cr, uid, ids, context=context)
	def create(self, cr, uid, vals, context=None):
		try:
			print 'CREA INVOICE '
			print vals
			centro_costo_id = 0
			purchase_id = 0
			doc_name = ""
			
			if vals['name']:
				doc_name = vals['name']
			elif vals['origin']:
				doc_name = vals['origin']

			print doc_name

			if doc_name:
				# BUSCAMOS EN VENTAS
				obj_sale_order_ids = self.pool.get('sale.order').search(cr, uid, [('name', '=', doc_name)])
				if len(obj_sale_order_ids) > 0:
					#print obj_sale_order_ids
					obj_sale_order = self.pool.get('sale.order').browse(cr, uid, obj_sale_order_ids)
					centro_costo_id = obj_sale_order[0]['centro_costo_id']['id']
				else:
					# BUSCAMOS EN COMPRAS
					obj_purchase_order_ids = self.pool.get('purchase.order').search(cr, uid, [('name', '=', doc_name)])
					if len(obj_purchase_order_ids) > 0:
						obj_purchase_order = self.pool.get('purchase.order').browse(cr, uid, obj_purchase_order_ids)
						centro_costo_id = obj_purchase_order[0]['centro_costo_id']['id']
					else:
						# BUSCAMOS EN ALBARANES DE ENTRADA
						obj_stock_pikcing_in_ids = self.pool.get('stock.picking.in').search(cr, uid, [('name', '=', doc_name)])
						if len(obj_stock_pikcing_in_ids) > 0:
							obj_stock_pikcing_in = self.pool.get('stock.picking.in').browse(cr, uid, obj_stock_pikcing_in_ids)
							#print 'ids stock in ' + str(obj_stock_pikcing_in)
							purchase_id = obj_stock_pikcing_in[0]['purchase_id']['id']
							#print 'compra id ' + str(purchase_id)
							obj_purchase_order = self.pool.get('purchase.order').browse(cr, uid, [purchase_id])
							centro_costo_id = obj_purchase_order[0]['centro_costo_id']['id']
						else:
							# BUSCAMOS EN ALBARANES DE SALIDA
							obj_stock_pikcing_out_ids = self.pool.get('stock.picking.out').search(cr, uid, [('name', '=', doc_name)])
							if len(obj_stock_pikcing_out_ids) > 0:
								obj_stock_pikcing_out = self.pool.get('stock.picking.out').browse(cr, uid, obj_stock_pikcing_out_ids)
								sale_id = obj_stock_pikcing_out[0]['sale_id']['id']
								obj_sale_order = self.pool.get('sale.order').browse(cr, uid, [sale_id])
								centro_costo_id = obj_sale_order[0]['centro_costo_id']['id']

			if centro_costo_id > 0:
				vals['centro_costo_id'] = centro_costo_id

		except Exception, e:
			print e
		finally:
			return super(account_invoice, self).create(cr, uid, vals, context=context)

	def write(self, cr, uid, ids, vals, context=None):
		print 'WRITE INVOICE '
		#obj_invoice = self.pool.get('account.invoice').read(cr, uid, ids)
		#print obj_invoice
		return super(account_invoice, self).write(cr, uid, ids, vals, context=context)

class account_move_line(osv.Model):
	_inherit = 'account.move.line'

	_columns = {
		'centro_costo_id': fields.many2one('account.cost.center', 'Centro de Costos', ondelete="cascade", required=True), 
	}

class account_move(osv.Model):
	_inherit = 'account.move'
