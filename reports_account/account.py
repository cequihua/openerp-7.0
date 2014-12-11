from openerp.osv import osv, fields
from tools.translate import _

class account_invoice(osv.Model):
	_inherit = 'account.account'

	_columns = {
		'account_category':fields.selection([('asset', 'Asset'),('liability','Liability'),
			('equity','Equity'),('income','Income'),('expense','Expense'),('cost','Cost'),('result','Result'),
			('balance_sheet','Balance Sheet'),('income_statement','Income Statement'),], 
			string="Category Account", required=False, readonly=True, help="Se utiliza para identificar el tipo de cuenta en los reportes contables"), 
	}