# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import netsvc
import time
from tools.translate import _

class balance_sheet_wizard(osv.osv_memory):
    _name = "wizard.balance.sheet"
    
    _columns = {
        #'afr_id': fields.many2one('afr', 'Custom Report', help='If you have already set a Custom Report, Select it Here.'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', help="Currency at which this report will be expressed. If not selected will be used the one set in the company"),
        'inf_type': fields.selection([('BS', 'Balance Sheet'), ('IS', 'Income Statement')], 'Type', required=True),
        'columns': fields.selection([('one', 'End. Balance'), ('two', 'Debit | Credit'), ('four', 'Initial | Debit | Credit | YTD'), ('five', 'Initial | Debit | Credit | Period | YTD'), ('qtr', "4 QTR's | YTD"), ('thirteen', '12 Months | YTD')], 'Columns', required=True),
        'display_account': fields.selection([('all', 'All Accounts'), ('bal', 'With Balance'), ('mov', 'With movements'), ('bal_mov', 'With Balance / Movements')], 'Display accounts'),
        'display_account_level': fields.integer('Up to level', help='Display accounts up to this level (0 to show all)'),

        #'account_list': fields.many2many('account.account', 'rel_wizard_account_balance', 'account_list', 'account_id', 'Root accounts', required=True),

        'fiscalyear': fields.many2one('account.fiscalyear', 'Fiscal year', help='Fiscal Year for this report', required=True),
        'periods': fields.many2many('account.period', 'rel_wizard_period_balance', 'wizard_id', 'period_id', 'Periods', help='All periods in the fiscal year if empty'),

        #'analytic_ledger': fields.boolean('Analytic Ledger', help="Allows to Generate an Analytic Ledger for accounts with moves. Available when Balance Sheet and 'Initial | Debit | Credit | YTD' are selected"),
        #'journal_ledger': fields.boolean('Journal Ledger', help="Allows to Generate an Journal Ledger for accounts with moves. Available when Balance Sheet and 'Initial | Debit | Credit | YTD' are selected"),
        #'partner_balance': fields.boolean('Partner Balance', help="Allows to "
        #                                 "Generate a Partner Balance for accounts with moves. Available when "
        #                                  "Balance Sheet and 'Initial | Debit | Credit | YTD' are selected"),
        'tot_check': fields.boolean('Summarize?', help='Checking will add a new line at the end of the Report which will Summarize Columns in Report'),
        'lab_str': fields.char('Description', help='Description for the Summary', size=128),

        'target_move': fields.selection([('posted', 'All Posted Entries'),
                                        ('all', 'All Entries'),
                                         ], 'Entries to Include', required=True,
                                        help='Print All Accounting Entries or just Posted Accounting Entries'),
        #~ Deprecated fields
        'filter': fields.selection([('bydate', 'By Date'), ('byperiod', 'By Period'), ('all', 'By Date and Period'), ('none', 'No Filter')], 'Date/Period Filter'),
        'date_to': fields.date('End date'),
        'date_from': fields.date('Start date'),
    }

    _defaults = {
        'date_from': lambda *a: time.strftime('%Y-%m-%d'),
        'date_to': lambda *a: time.strftime('%Y-%m-%d'),
        'filter': lambda *a: 'byperiod',
        #'display_account_level': lambda *a: 0,
        'inf_type': lambda *a: 'BS',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
        'fiscalyear': lambda self, cr, uid, c: self.pool.get('account.fiscalyear').find(cr, uid),
        'display_account': lambda *a: 'bal_mov',
        'columns': lambda *a: 'five',
        'target_move': 'posted',
        'currency_id': lambda self, cr, uid, c: self.pool.get('res.currency').search(cr, uid,[('name','=','MXN')])[0],
    }
    def period_span(self, cr, uid, ids, fy_id, context=None):
        if context is None:
            context = {}
        ap_obj = self.pool.get('account.period')
        fy_id = fy_id and type(fy_id) in (list, tuple) and fy_id[0] or fy_id
        if not ids:
            #~ No hay periodos
            return ap_obj.search(cr, uid, [('fiscalyear_id', '=', fy_id), ('special', '=', False)], order='date_start asc')

        ap_brws = ap_obj.browse(cr, uid, ids, context=context)
        date_start = min([period.date_start for period in ap_brws])
        date_stop = max([period.date_stop for period in ap_brws])

        return ap_obj.search(cr, uid, [('fiscalyear_id', '=', fy_id), ('special', '=', False), ('date_start', '>=', date_start), ('date_stop', '<=', date_stop)], order='date_start asc')

    def print_report(self, cr, uid, ids, data, context=None):
        name = 'balance.sheet.mako'
        if context is None:
            context = {}

        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids[0])

        if data['form']['filter'] == 'byperiod':
            del data['form']['date_from']
            del data['form']['date_to']
            data['form']['periods'] = self.period_span(cr, uid, data['form']['periods'], data['form']['fiscalyear'])

        return {'type': 'ir.actions.report.xml', 'report_name': name, 'datas': data, 'report_type': 'webkit'}

balance_sheet_wizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: