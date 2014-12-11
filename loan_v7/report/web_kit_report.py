from report import report_sxw
from openerp.osv import osv, fields
import pdb

class web_kit_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(web_kit_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_loan': self.get_loan,
            'get_loan_payment': self.get_loan_payment,
            'get_report_general': self.get_report_general,
        })
       
    def get_loan(self, form):
        return True
              
    def get_loan_payment(self, form): 
        form['form']          
        loan_payment_ids = self.pool.get('loan.payment').search(self.cr, self.uid, [('id','=',form['form']['periodo_id'][0])])
        loan_payment_objs = self.pool.get('loan.payment').browse(self.cr, self.uid, loan_payment_ids)                                    
        return loan_payment_objs

    def get_report_general(self, form):
        res = {}
        pdb.set_trace()
        invoices_prov_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('type', '=', 'in_invoice')])
        invoices_account_prov_obj = self.pool.get('account.invoice').browse(self.cr, self.uid, invoices_prov_ids)
        for i in invoices_account_prov_obj:
            invoices_cli_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('type', '=', 'out_invoice'),('loan_id', '=',i.loan_id),('is_general', '=', True)])
            invoices_account_cli_obj = self.pool.get('account.invoice').browse(self.cr, self.uid, i.invoices_cli_ids)
            res.apppend({
                'cliente':invoices_account_cli_obj['partner_id'][1],
                'credito': invoices_account_cli_obj['loan_id'][1],
                'monto_cli': invoices_account_cli_obj['amount_total'],
                'abono_cli': invoices_account_cli_obj['amount_total'] - invoices_account_cli_obj['residual'],
                'saldo_cli': invoices_account_cli_obj['residual'],
                'proveedor': i.partner_id.name,
                'monto_pro': i.amount_total,
                'abono_pro': i.amount_total - i.residual,
                'saldo_pro': i.residual,
                })
        return res
    
report_sxw.report_sxw('report.estadocuenta.account.loan', 'account.loan', 'loan_v7/report/estado_cuenta.mako', parser=web_kit_report)
report_sxw.report_sxw('report.general.account.loan', 'account.loan', 'loan_v7/report/general_report.mako', parser=web_kit_report)