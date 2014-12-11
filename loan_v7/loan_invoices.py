import time
#import datetime
from datetime import datetime
import pooler
from decimal import *
# from osv import osv
# from osv import fields
from datetime import date
from openerp.osv import osv, fields
import pdb

class invoices(osv.Model):
	_inherit = 'account.invoice'
	_columns = {
		'loan_id': fields.many2one('account.loan', string="Loan", ondelete='cascade'),
		'loan_payment_id': fields.many2one('loan.payment', string="Amortizacion", ondelete="cascade"),
		'is_general': fields.boolean(string="General"),
	}
	_defaults = {
		'is_general': False,
	}
class account_voucher(osv.Model):
	_inherit = 'account.voucher'
	_columns = {
		'loan_payment_id': fields.many2one('loan.payment', string="Corte", required=False, ondelete="cascade"),
		'iva': fields.float('IVA',digits=(12,2), readonly=True),
		'int': fields.float('Interes',digits=(12,2),readonly=True),
		'cap': fields.float('Capital',digits=(12,2),readonly=True),
		'saldo_pen': fields.float('Saldo Pendiente', digits=(12,2), readonly=True),
	}

	def onchange_payment(self, cr, uid, ids, payment_id):
		pay_loan_obj = self.pool.get('loan.payment').read(cr,uid,payment_id)
		amount = pay_loan_obj['pago_mes']
		cap = pay_loan_obj['capital_mes']
		_int = pay_loan_obj['interes']
		iva = pay_loan_obj['interes'] * 0.16
		sal_pen = pay_loan_obj['saldo_pen']

		return {'value': {'amount': amount,'cap':cap, 'int': _int, 'iva': iva, 'saldo_pen':sal_pen}}

	def button_proforma_voucher(self, cr, uid, ids, context=None):
		super(account_voucher, self).button_proforma_voucher(cr, uid, ids, context=context)
		try:
			saldo = 0
			saldo_pen = 0
			state = ''
			iva = 0
			loan_payment_id = 0
			pay = self.pool.get('account.voucher').read(cr,uid,ids)
			invoice_id = context.get('invoice_id', False)
			invoice_obj = self.pool.get('account.invoice').read(cr,uid,invoice_id)
			#print pay
			#pdb.set_trace()
			if pay[0]['loan_payment_id']:
				loan_payment_id = pay[0]['loan_payment_id'][0]
			else:
				payment_ids = self.pool.get('loan.payment').search(cr,uid, [('loan_id','=',invoice_obj['loan_id'][0]),('state','=','pending'),('saldo_pen','>',0)])
				payments_obj = self.pool.get('loan.payment').browse(cr,uid,payment_ids)
				for p in payments_obj:
					saldo_pen += p.saldo_pen

				loan_payment_id = invoice_obj['loan_payment_id'][0]
				loan_payment_obj = self.pool.get('loan.payment').read(cr,uid,loan_payment_id)
				iva = (loan_payment_obj['interes'] + saldo_pen) * 0.16
				saldo = (iva  + loan_payment_obj['interes'] + saldo_pen) - (pay[0]['amount'])
			# acc_loan = self.pool.get('account.loan').read(cr,uid,invoice_obj['loan_id'][0])
			# loan_id = invoice_obj['loan_id'][0]
			# loan_payment_id = invoice_obj['loan_payment_id'][0]
			
			if saldo > 0:
				state = 'pending'
			else:
				state = 'paid'
				if pay[0]['loan_payment_id'] == False:
					loan_payment_ids = self.pool.get('loan.payment').search(cr,uid,[('loan_id', '=', invoice_obj['loan_id'][0]), ('saldo_pen','>',0)])
					self.pool.get('loan.payment').write(cr,uid,loan_payment_ids,{'state':state, 'saldo_pen': saldo})
			# #print loan_payment_obj
			# amount_pay = loan_payment_obj['pago_mes']
			# account_id_credit = acc_loan['loan_acc'][0]
			# account_id_debit = acc_loan['bank_acc'][0]
			# amount_pay += loan_payment_obj['interes']
			# journal_id = invoice_obj['journal_id'][0]

			# account_move_id = self.pool.get('account.move').create(cr,uid,{'name':acc_loan['loan_id'],'journal_id':journal_id, 'period_id':10, 'date':date.today()})
			# self.pool.get('account.move.line').create(cr,uid,{'move_id': account_move_id, 'journal_id':journal_id, 'period_id':10, 'date':date.today(), 'name': acc_loan['loan_id'], 'account_id':account_id_credit,'debit':0, 'credit':amount_pay, 'acc_loan_id':loan_id})
			# self.pool.get('account.move.line').create(cr,uid,{'move_id': account_move_id, 'journal_id':journal_id, 'period_id':10, 'date':date.today(), 'name': acc_loan['loan_id'], 'account_id':account_id_debit,'debit':amount_pay, 'credit':0, 'acc_loan_id':loan_id})
			
			self.pool.get('loan.payment').write(cr,uid,loan_payment_id,{'state':state, 'saldo_pen': saldo})
			# self.pool.get('account.invoice').write(cr, uid, invoice_id, {'state':'paid'})
		except Exception, e:
			print 'ERROR button_proforma_voucher ' + str(e)
		finally:
			return True
		
class loan_payment(osv.Model):
	_name = 'loan.payment'
	_rec_name = 'fecha'
	_columns = {
		'no_mes': fields.integer(string='Periodo'),
		'capital': fields.float('Saldo Inicial',digits=(12,2)),
		'interes': fields.float('Intereses',digits=(12,2)),
		'pago_mes': fields.float('Pago Mensual', digits=(12,2)),
		'capital_mes': fields.float('Capital', digits=(12,2)),
		'pago_capital': fields.float('Pago Total',digits=(12,2)),
		'saldo_con_interes': fields.float('Saldo con Intereses', digits=(12,2)),
		'saldo': fields.float('Saldo Final',digits=(12,2)),
		'saldo_pen': fields.float('Saldo Pendiente',digits=(12,2)),
		'loan_id': fields.many2one('account.loan', string="Prestamo", ondelete='cascade'),
		'fecha': fields.date('Fecha de Corte'),
		'invoice_ids':fields.one2many('account.invoice','loan_payment_id','Invoices'),
		'state': fields.selection([
           ('pending','Pendiente'),
           ('paid','Pagado'),
        ],'State', readonly=True, select=True),
	}

	_defaults = {
		'state': '',
	}
	
	def create_invoice_pay(self, cr, uid, ids, context={}):
		pay_loan = self.pool.get('loan.payment').read(cr, uid, ids)
		#print pay_loan[0]
		loan_id = pay_loan[0]['loan_id'][0]
		acc_loan = self.pool.get('account.loan').read(cr, uid, loan_id)
		partner_id = acc_loan['partner_id'][0]
		fecha = pay_loan[0]['fecha']
		saldo = 0
		payment_ids = self.pool.get('loan.payment').search(cr,uid, [('loan_id','=',loan_id),'|',('saldo_pen','>',0),('saldo_pen','<',0)])
		payments_obj = self.pool.get('loan.payment').browse(cr,uid,payment_ids)
		for p in payments_obj:
			saldo += p.saldo_pen

		interes_product_id = self.pool.get('product.product').search(cr,uid,[('name','=','Intereses')])
		capital_product_id = self.pool.get('product.product').search(cr,uid,[('name','=','Capital')])
		#if saldo > 0:
			#saldo_pen_product_id: = self.pool.get('product.product').search(cr,uid,[('name','=','Saldo Pendiente')])

		#account_int = self.pool.get('product.product').read(cr, uid, interes_product_id)
		#account_cap = self.pool.get('product.product').read(cr, uid, capital_product_id)
		account_cap_id = acc_loan['cob_acc'][0] #account_int[0]['property_account_income'][0]
		account_int_id = acc_loan['int_acc'][0] #account_cap[0]['property_account_income'][0]

		int_journal_id = self.pool.get('account.journal').search(cr,uid,[('code','=','INT')])[0]
		cap_journal_id = self.pool.get('account.journal').search(cr,uid,[('code','=','CAP')])[0]

		currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','MXN')])[0]

		invoice_int_id = self.pool.get('account.invoice').create(cr, uid,{'loan_payment_id':ids[0],'partner_id' : partner_id, 'date_invoice' : fecha, 'state': 'draft', 'account_id':account_cap_id, 'company_id': 1, 'currency_id':currency_id, 'journal_id':int_journal_id, 'reference_type': 'none', 'loan_id': loan_id})
		#invoice_cap_id = self.pool.get('account.invoice').create(cr, uid,{'loan_payment_id':ids[0],'partner_id' : partner_id, 'date_invoice' : fecha, 'state': 'draft', 'account_id':account_cap_id, 'company_id': 1, 'currency_id':currency_id, 'journal_id':cap_journal_id, 'reference_type': 'none', 'loan_id': loan_id})
		
		#print capital_product_id
		#print interes_product_id
		
		intereses = pay_loan[0]['interes'] + saldo
		capital = pay_loan[0]['pago_mes']
		
		#self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_cap_id,'name' : 'Capital', 'product_id' : capital_product_id[0], 'price_unit': capital, 'quantity': 1, 'account_id':account_cap_id})
		self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_int_id,'name' : 'Intereses', 'product_id' : interes_product_id[0], 'price_unit': intereses, 'quantity': 1, 'account_id':account_int_id})
		#self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_int_id,'name' : 'Intereses', 'product_id' : interes_product_id[0], 'price_unit': intereses, 'quantity': 1, 'account_id':account_int_id})
		return True

	def calculate_int(self, cr, uid, ids, context={}):
		return True
		
class loan_invoices(osv.Model):
	_inherit = 'account.loan'
	_columns = {
		'invoice_ids':fields.one2many('account.invoice','loan_id','Invoices'),
		'payment_ids':fields.one2many('loan.payment','loan_id','Payments'),
	}

	def approve_finance(self, cr, uid, ids, context={}):
		self.write(cr,uid,ids,{'state':'proof approval'})
		return True

	def cancel(self, cr, uid, ids, context={}):
		self.write(cr,uid,ids,{'state':'cancel'})
		return True

	def create_policy(self, cr, uid, ids, context={}):
		acc_loan = self.pool.get('account.loan').read(cr,uid,ids)
		monto = 0.0
		monto = acc_loan[0]['loan_amount']
		payment_ids = acc_loan[0]['payment_ids']
		pay_loan_objs = self.pool.get('loan.payment').browse(cr, uid, payment_ids)
		date_credit = acc_loan[0]['approve_date']
		date_credit = datetime.strptime(date_credit, '%Y-%m-%d').date()
		print date_credit
		month = date_credit.month
		year = date_credit.year
		day = date_credit.day

		for p in pay_loan_objs:
			#pdb.set_trace()
			if month > 12:
				year += 1
				month = 1
			if month == 2:
				if date_credit.day > 29:
					date_credit = date_credit.replace(day=28)
					date_credit = date_credit.replace(month=month)
					date_credit = date_credit.replace(year=year)
				else:
					date_credit = date_credit.replace(month=month)
					date_credit = date_credit.replace(year=year)
					date_credit = date_credit.replace(day=day)
			else:
				date_credit = date_credit.replace(month=month)
				date_credit = date_credit.replace(year=year)
				date_credit = date_credit.replace(day=day)
			self.pool.get('loan.payment').write(cr,uid,p.id,{'fecha':date_credit})
			month += 1
		#print acc_loan[0]
		account_id_credit = acc_loan[0]['cus_pay_acc'][0]
		account_id_debit = acc_loan[0]['bank_acc'][0]

		#account_move_id = self.pool.get('account.move').create(cr,uid,{'name':acc_loan[0]['loan_id'],'journal_id':11, 'period_id':10, 'date':date.today()})
		#self.pool.get('account.move.line').create(cr,uid,{'move_id': account_move_id, 'journal_id':11, 'period_id':10, 'date':date.today(), 'name': acc_loan[0]['loan_id'], 'account_id':account_id_credit,'debit':monto, 'credit':0, 'acc_loan_id':ids[0]})
		#self.pool.get('account.move.line').create(cr,uid,{'move_id': account_move_id, 'journal_id':11, 'period_id':10, 'date':date.today(), 'name': acc_loan[0]['loan_id'], 'account_id':account_id_debit,'debit':0, 'credit':monto, 'acc_loan_id':ids[0]})
		
		capital_product_id = self.pool.get('product.product').search(cr,uid,[('name','=','Capital')])
		account_cap_id = acc_loan[0]['loan_acc'][0] #account_int[0]['property_account_income'][0]
		#account_int_id = acc_loan[0]['int_acc'][0] #account_cap[0]['property_account_income'][0]

		#int_journal_id = self.pool.get('account.journal').search(cr,uid,[('code','=','INT')])[0]
		cap_journal_id = self.pool.get('account.journal').search(cr,uid,[('code','=','CAP')])[0]

		currency_id = self.pool.get('res.currency').search(cr,uid,[('name','=','MXN')])[0]

		#invoice_int_id = self.pool.get('account.invoice').create(cr, uid,{'loan_payment_id':ids[0],'partner_id' : partner_id, 'date_invoice' : date.today(), 'state': 'draft', 'account_id':cap_journal_id, 'company_id': 1, 'currency_id':currency_id, 'journal_id':int_journal_id, 'reference_type': 'none', 'loan_id': loan_id})
		invoice_cap_id = self.pool.get('account.invoice').create(cr, uid,{'partner_id' : acc_loan[0]['partner_id'][0], 'date_invoice' : date.today(), 'state': 'draft', 'account_id':account_cap_id, 'company_id': 1, 'currency_id':currency_id, 'journal_id':cap_journal_id, 'reference_type': 'none', 'loan_id': ids[0], 'is_general':True})
		
		#print capital_product_id
		#print interes_product_id
		
		#intereses = pay_loan[0]['interes']
		capital = acc_loan[0]['loan_amount']
		
		self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_cap_id,'name' : 'Capital', 'product_id' : capital_product_id[0], 'price_unit': capital, 'quantity': 1, 'account_id':account_id_debit})
		#self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_int_id,'name' : 'Intereses', 'product_id' : interes_product_id[0], 'price_unit': intereses, 'quantity': 1, 'account_id':account_int_id})


		self.write(cr,uid,ids,{'state':'approved'})
		# self.pool.get('loan.payment').write(cr, uid, payment_ids, {'fecha':acc_loan['approve_date']})
		return True

	def create_invoices(self, cr, uid, ids, context={}):
		#pdb.set_trace()
		acc_loan = self.pool.get('account.loan').read(cr,uid,ids)
		loan_payment_ids = acc_loan[0]['payment_ids']
		partner_id = acc_loan[0]['partner_id'][0]
		#print loan_payment_ids
		loan_id = ids[0]
		capital = 0.0
		intereses = 0.0

		objs_loan_payment = self.pool.get('loan.payment').browse(cr,uid,loan_payment_ids)
		interes_product_id = self.pool.get('product.product').search(cr,uid,[('name','=','Intereses')])
		capital_product_id = self.pool.get('product.product').search(cr,uid,[('name','=','Capital')])

		fecha = date.today()
		#print fecha
		i = 1
		for p in objs_loan_payment:
			invoice_id = self.pool.get('account.invoice').create(cr, uid,{'partner_id' : partner_id, 'date_invoice' : fecha, 'state': 'draft', 'account_id':174, 'company_id': 1, 'currency_id':1, 'journal_id':1, 'reference_type': 'none', 'loan_id': loan_id})
			intereses = p.interes
			capital = p.pago_mes

			self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_id,'name' : 'Intereses', 'product_id' : interes_product_id[0], 'price_unit': intereses, 'quantity': 1})
			self.pool.get('account.invoice.line').create(cr, uid,{'invoice_id' : invoice_id,'name' : 'Capital', 'product_id' : capital_product_id[0], 'price_unit': capital, 'quantity': 1})
		
		self.write(cr,uid,ids,{'state':'approved'})
		return True

	def create_amortization_table(self, cr, uid, ids, amount, rate, time, loan_id):
		meses = time
		saldo_inicial = 0.0
		saldo_final = 0.0
		int_saldo_insoluto = 0.0
		saldo_con_interes = 0.0
		taza = rate
		monto = amount
		amortizacion = 0.0
		pago_total = 0.0
		saldo_final = 0.0
		capital = 0.0
		#pdb.set_trace()
		pago_mensual = monto/meses
		saldo_inicial = saldo_inicial + monto
		saldo_final = saldo_final + monto

		loan_payment_cr = None
		account_loan = self.pool.get('account.loan').read(cr, uid, ids)
		loan_payment_ids = account_loan[0]['payment_ids']

		if loan_payment_ids:
			loan_payment_cr = self.pool.get('loan.payment')
			loan_payment_cr.unlink(cr,uid,loan_payment_ids)

		i = 1
		for num in range(meses):
			if i>1:
				saldo_inicial = saldo_inicial - pago_mensual
			#print taza
			int_saldo_insoluto = (saldo_inicial * taza)/100
			saldo_con_interes = saldo_inicial + int_saldo_insoluto
			amortizacion = pago_mensual
			pago_total = amortizacion + int_saldo_insoluto
			saldo_final = saldo_final - pago_mensual
			capital = amortizacion - int_saldo_insoluto

			self.pool.get('loan.payment').create(cr, uid, {'no_mes': i, 'capital': saldo_inicial, 'capital_mes': capital, 'interes': int_saldo_insoluto, 'saldo_con_interes': saldo_con_interes, 'pago_mes': amortizacion, 'pago_capital': pago_total, 'saldo': saldo_final, 'loan_id': loan_id})
			i+=1
		return True

	