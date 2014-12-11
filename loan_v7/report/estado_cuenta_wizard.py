# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import netsvc

class wizard_estado_cuenta_report(osv.osv_memory):
	_name = "wizard.estadocuenta.account.loan.report"

	_columns = {
		'loan_id': fields.many2one('account.loan', string="Credito"),
		'periodo_id': fields.many2one('loan.payment', string="Periodo", domain="[('loan_id','=',loan_id),('state','=','pending')]"),
	}

	def print_report(self, cr, uid, ids, context=None):
		datas = {'ids': context.get('active_ids', [])}
		datas['model'] = 'wizard.estadocuenta.account.loan.report'
		datas['form'] = self.read(cr, uid, ids)[0]
		report = 'report.estadocuenta.account.loan'

		return {
    		'type': 'ir.actions.report.xml',
    		'report_name': report,
    		'report_type': 'webkit',
    		'datas': datas,
		}

class wizard_general_report(osv.osv_memory):
	_name = "wizard.general.loan.report"

	_columns = {
		'name': fields.char('Nombre'),
		'fecha_ini': fields.date('Fecha Inicio'),
		'fecha_fin': fields.date('Fecha Final'),
	}

	def print_report(self, cr, uid, ids, context=None):
		datas = {'ids': context.get('active_ids', [])}
		datas['model'] = 'wizard.general.loan.report'
		datas['form'] = self.read(cr, uid, ids)[0]
		report = 'report.general.account.loan'

		return {
    		'type': 'ir.actions.report.xml',
    		'report_name': report,
    		'report_type': 'webkit',
    		'datas': datas,
		}