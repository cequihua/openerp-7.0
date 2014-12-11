import time
from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import osv, fields
import pdb

class web_kit_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(web_kit_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_loan': self.get_loan,
            'get_loan_payment': self.get_loan_payment,
            'get_loan_payments': self.get_loan_payments,
            'get_capital_total': self.get_capital_total,
            'get_report_general': self.get_report_general,
            'get_saldo_pen_total': self.get_saldo_pen_total,
        })
       
    def get_loan(self, form):
        loan_id = self.pool.get('account.loan').search(self.cr, self.uid, [('id','=',form['form']['loan_id'][0])])
        loan_payment_obj = self.pool.get('account.loan').browse(self.cr, self.uid, loan_id)                                    
        return loan_payment_obj
              
    def get_loan_payment(self, form): 
        #print form['form']          
        loan_payment_ids = self.pool.get('loan.payment').search(self.cr, self.uid, [('id','=',form['form']['periodo_id'][0])])
        loan_payment_objs = self.pool.get('loan.payment').browse(self.cr, self.uid, loan_payment_ids)                                    
        return loan_payment_objs

    def get_loan_payments(self, form): 
        #print form['form']          
        loan_payment_ids = self.pool.get('loan.payment').search(self.cr, self.uid, [('loan_id','=',form['form']['loan_id'][0]), ('state','in',['paid','pending'])])
        loan_payment_objs = self.pool.get('loan.payment').browse(self.cr, self.uid, loan_payment_ids)                                    
        return loan_payment_objs

    def get_capital_total(self, form):
        loan_payment_ids = self.pool.get('loan.payment').search(self.cr, self.uid, [('loan_id','=',form['form']['loan_id'][0]), ('state','=','pending')])
        loan_payment_objs = self.pool.get('loan.payment').browse(self.cr, self.uid, loan_payment_ids)
        
        total = 0
        for p in loan_payment_objs:
            total += p.pago_mes
        return total

    def get_saldo_pen_total(self, form):
        loan_payment_ids = self.pool.get('loan.payment').search(self.cr, self.uid, [('loan_id','=',form['form']['loan_id'][0])])
        loan_payment_objs = self.pool.get('loan.payment').browse(self.cr, self.uid, loan_payment_ids)
        
        total = 0
        for p in loan_payment_objs:
            total += p.saldo_pen
        return total        

    def get_report_general(self, form):
        res = []
        #pdb.set_trace()
        invoices_prov_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('type', '=', 'in_invoice'), ('loan_id', '!=', False)])
        invoices_account_prov_obj = self.pool.get('account.invoice').browse(self.cr, self.uid, invoices_prov_ids)
        for i in invoices_account_prov_obj:
            invoices_cli_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('type', '=', 'out_invoice'),('loan_id', '=',i['loan_id']['id']),('is_general', '=', True)])
            invoices_account_cli_obj = self.pool.get('account.invoice').browse(self.cr, self.uid, invoices_cli_ids)
            res.append({
                'cliente':invoices_account_cli_obj[0]['partner_id']['name'],
                'credito': invoices_account_cli_obj[0]['loan_id']['loan_id'],
                'monto_cli': invoices_account_cli_obj[0]['amount_total'],
                'abono_cli': invoices_account_cli_obj[0]['amount_total'] - invoices_account_cli_obj[0]['residual'],
                'saldo_cli': invoices_account_cli_obj[0]['residual'],
                'proveedor': i['partner_id']['name'],
                'monto_pro': i['amount_total'],
                'abono_pro': i['amount_total'] - i['residual'],
                'saldo_pro': i['residual'],
                })
        return res

    
report_sxw.report_sxw('report.estadocuenta.account.loan', 'account.loan', 'addons/loan_v7/report/estado_cuenta.mako', parser=web_kit_report)
report_sxw.report_sxw('report.general.account.loan', 'account.loan', 'addons/loan_v7/report/general_report.mako', parser=web_kit_report)