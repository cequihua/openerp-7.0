## -*- coding: utf-8 -*-
from report import report_sxw
#from account_financial_report.report.parser import account_balance
from tools.translate import _
import time
import pdb
import math

class balance_sheet_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(balance_sheet_parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'get_fiscalyear_text': self.get_fiscalyear_text,
            'get_periods_and_date_text': self.get_periods_and_date_text,
            'get_informe_text': self.get_informe_text,
            'get_month':self.get_month,
            'exchange_name':self.exchange_name,
            'get_company_logo':self.get_company_logo,
            'to_money':self.to_money,
        })
        self.context = context

    def get_fiscalyear_text(self, form):
        """
        Returns the fiscal year text used on the report.
        """
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        fiscalyear = None
        if form.get('fiscalyear'):
            fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, form['fiscalyear'])
            return fiscalyear.name or fiscalyear.code
        else:
            fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, fiscalyear_obj.find(self.cr, self.uid))
            return "%s*" % (fiscalyear.name or fiscalyear.code)

    def get_informe_text(self, form):
        """
        Returns the header text used on the report.
        """
        name = "Balance General"
        return name

    def get_month(self, form):
        '''
        return day, year and month
        '''
        if form['filter'] in ['bydate', 'all']:
            months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            mes = months[time.strptime(form['date_to'],"%Y-%m-%d")[1]-1]
            ano = time.strptime(form['date_to'],"%Y-%m-%d")[0]
            dia = time.strptime(form['date_to'],"%Y-%m-%d")[2]
            return _('From ')+self.formatLang(form['date_from'], date=True)+ _(' to ')+self.formatLang(form['date_to'], date=True)
        elif form['filter'] in ['byperiod', 'all']:
            aux=[]
            period_obj = self.pool.get('account.period')
            
            for period in period_obj.browse(self.cr, self.uid, form['periods']):
                aux.append(period.date_start)
                aux.append(period.date_stop)
            sorted(aux)
            return _('DE ')+self.formatLang(aux[0], date=True)+_(' HASTA ')+self.formatLang(aux[-1], date=True)

    def get_periods_and_date_text(self, form):
        """
        Returns the text with the periods/dates used on the report.
        """
        period_obj = self.pool.get('account.period')
        periods_str = None
        fiscalyear_id = form['fiscalyear'] or fiscalyear_obj.find(self.cr, self.uid)
        period_ids = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear_id),('special','=',False)])
        if form['filter'] in ['byperiod', 'all']:
            period_ids = form['periods']
        periods_str = ', '.join([period.name or period.code for period in period_obj.browse(self.cr, self.uid, period_ids)])
        dates_str = None
        if form['filter'] in ['bydate', 'all']:
            dates_str = self.formatLang(form['date_from'], date=True) + ' - ' + self.formatLang(form['date_to'], date=True) + ' '
        return {'periods':periods_str, 'date':dates_str}


    def special_period(self, periods):
        period_obj = self.pool.get('account.period')
        period_brw = period_obj.browse(self.cr, self.uid, periods)
        period_counter = [True for i in period_brw if not i.special]
        if not period_counter:
            return True
        return False
        
    def exchange_name(self, form):
        self.from_currency_id = self.get_company_currency(form['company_id'] and type(form['company_id']) in (list,tuple) and form['company_id'][0] or form['company_id'])
        if not form['currency_id']:
            self.to_currency_id = self.from_currency_id
        else:
            self.to_currency_id = form['currency_id'] and type(form['currency_id']) in (list, tuple) and form['currency_id'][0] or form['currency_id']
        return self.pool.get('res.currency').browse(self.cr, self.uid, self.to_currency_id).name

    def exchange(self, from_amount):
        if self.from_currency_id == self.to_currency_id:
            return from_amount
        curr_obj = self.pool.get('res.currency')
        return curr_obj.compute(self.cr, self.uid, self.from_currency_id, self.to_currency_id, from_amount)
    
    def get_company_currency(self, company_id):
        rc_obj = self.pool.get('res.company')
        return rc_obj.browse(self.cr, self.uid, company_id).currency_id.id

    def get_company_logo(self, form):
        #print form['company_id']
        #pdb.set_trace()
        res = {}
        rc_obj = self.pool.get('res.company')
        company_obj = rc_obj.read(self.cr, self.uid, form['company_id'][0])

        # res = {
        #     'logo':company_obj['logo'],
        #     'name':company_obj['name'],
        # }
        return company_obj['logo']
    
    def get_company_accounts(self, company_id, acc='credit'):
        rc_obj = self.pool.get('res.company')
        if acc=='credit':
            return [brw.id for brw in rc_obj.browse(self.cr, self.uid, company_id).credit_account_ids]
        else:
            return [brw.id for brw in rc_obj.browse(self.cr, self.uid, company_id).debit_account_ids]

    def to_money(self,amount):
        return format(math.floor(amount * 100) / 100, ',.2f')

    def lines(self, form, level=0):
        """
        Returns all the data needed for the report lines
        (account info plus debit/credit/balance in the selected period
        and the full year)
        """
        account_obj = self.pool.get('account.account')
        period_obj = self.pool.get('account.period')
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        #cost_center_pool = self.pool.get('account.cost.center')
        journal_pool = self.pool.get('account.journal')

        def _get_children_and_consol(cr, uid, ids, level, context={},change_sign=False):
            aa_obj = self.pool.get('account.account')
            ids2=[]
            for aa_brw in aa_obj.browse(cr, uid, ids, context):
                if aa_brw.child_id and aa_brw.level < level and aa_brw.type !='consolidation':
                    if not change_sign:
                        ids2.append([aa_brw.id,True, False,aa_brw,aa_brw.account_category])
                    ids2 += _get_children_and_consol(cr, uid, [x.id for x in aa_brw.child_id], level, context,change_sign=change_sign)
                    if change_sign:
                        ids2.append(aa_brw.id) 
                    else:
                        ids2.append([aa_brw.id,False,True,aa_brw,aa_brw.account_category])
                else:
                    if change_sign:
                        ids2.append(aa_brw.id) 
                    else:
                        ids2.append([aa_brw.id,True,True,aa_brw,aa_brw.account_category])
            return ids2

        #############################################################################
        # CONTEXT FOR ENDIND BALANCE                                                #
        #############################################################################

        def _ctx_end(ctx):
            ctx_end = ctx
            ctx_end['filter'] = form.get('filter','all')
            ctx_end['fiscalyear'] = fiscalyear.id
            if ctx_end['filter'] not in ['bydate','none']:
                special = self.special_period(form['periods'])
            else:
                special = False
            if form['filter'] in ['byperiod', 'all']:
                if special:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['periods'] or ctx_end.get('periods',False))])
                else:
                    ctx_end['periods'] = period_obj.search(self.cr, self.uid, [('id','in',form['periods'] or ctx_end.get('periods',False)),('special','=',False)])
                    
            if form['filter'] in ['bydate','all','none']:
                ctx_end['date_from'] = form['date_from']
                ctx_end['date_to'] = form['date_to']
            
            return ctx_end.copy()
        
        def missing_period(ctx_init):
            
            ctx_init['fiscalyear'] = fiscalyear_obj.search(self.cr, self.uid, [('date_stop','<',fiscalyear.date_start)],order='date_stop') and \
                                fiscalyear_obj.search(self.cr, self.uid, [('date_stop','<',fiscalyear.date_start)],order='date_stop')[-1] or []
            ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',ctx_init['fiscalyear']),('date_stop','<',fiscalyear.date_start)])
            return ctx_init
        #############################################################################
        # CONTEXT FOR INITIAL BALANCE                                               #
        #############################################################################
        
        def _ctx_init(ctx):
            ctx_init = self.context.copy()
            ctx_init['filter'] = form.get('filter','all')
            ctx_init['fiscalyear'] = fiscalyear.id

            if form['filter'] in ['byperiod', 'all']:
                ctx_init['periods'] = form['periods']
                if not ctx_init['periods']:
                    ctx_init = missing_period(ctx_init.copy())
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('date_stop','<=',date_start)])
            elif form['filter'] in ['bydate']:
                ctx_init['date_from'] = fiscalyear.date_start
                ctx_init['date_to'] = form['date_from']
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('date_stop','<=',ctx_init['date_to'])])
            elif form['filter'] == 'none':
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('special','=',True)])
                date_start = min([period.date_start for period in period_obj.browse(self.cr, self.uid, ctx_init['periods'])])
                ctx_init['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('date_start','<=',date_start),('special','=',True)])
            
            return ctx_init.copy()

        def z(n):
            return abs(n) < 0.005 and 0.0 or n
                
        #print form
        self.from_currency_id = self.get_company_currency(form['company_id'] and type(form['company_id']) in (list,tuple) and form['company_id'][0] or form['company_id'])
        if not form['currency_id']:
            self.to_currency_id = self.from_currency_id
        else:
            self.to_currency_id = form['currency_id'] and type(form['currency_id']) in (list, tuple) and form['currency_id'][0] or form['currency_id']
        
        account_ids = []
        #get everithing account of balance
        sql_accounts = """select id, code from account_account where account_category in ('asset', 'liability', 'equity')
                            union
                        select id, code from account_account where account_category in ('balance_sheet') order by code"""
        self.cr.execute(sql_accounts)
        account_res = self.cr.dictfetchall()
        for a in account_res:
            account_ids.append(a['id'])

        # if form.has_key('account_list') and form['account_list']:
        #     account_ids = form['account_list']
        #     del form['account_list']
        
        #credit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list,tuple) and form['company_id'][0] or form['company_id'],'credit')
        
        #debit_account_ids = self.get_company_accounts(form['company_id'] and type(form['company_id']) in (list,tuple) and form['company_id'][0] or form['company_id'],'debit')
        credit_account_ids = []
        debit_account_ids = []

        if form.get('fiscalyear'):
            if type(form.get('fiscalyear')) in (list,tuple):
                fiscalyear = form['fiscalyear'] and form['fiscalyear'][0]
            elif type(form.get('fiscalyear')) in (int,):
                fiscalyear = form['fiscalyear']
        fiscalyear = fiscalyear_obj.browse(self.cr, self.uid, fiscalyear)

        ################################################################
        # Get the accounts                                             #
        ################################################################
        #pdb.set_trace()
        account_ids = _get_children_and_consol(self.cr, self.uid, account_ids, 0,self.context)
        
        credit_account_ids = _get_children_and_consol(self.cr, self.uid, credit_account_ids, 100,self.context,change_sign=True)
        
        debit_account_ids = _get_children_and_consol(self.cr, self.uid, debit_account_ids, 100,self.context,change_sign=True)
        
        credit_account_ids = list(set(credit_account_ids) - set(debit_account_ids))

        #
        # Generate the report lines (checking each account)
        #
        
        if not form['periods']:
            form['periods'] = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('special','=',False)],order='date_start asc')
            if not form['periods']:
                raise osv.except_osv(_('UserError'),_('The Selected Fiscal Year Does not have Regular Periods'))

        if form['columns'] == 'qtr':
            period_ids = period_obj.search(self.cr, self.uid, [('fiscalyear_id','=',fiscalyear.id),('special','=',False)],order='date_start asc')
            a=0
            l=[]
            p=[]
            for x in period_ids:
                a+=1
                if a<3:
                        l.append(x)
                else:
                        l.append(x)
                        p.append(l)
                        l=[]
                        a=0
            
        ctx_init = _ctx_init(self.context.copy())
        ctx_end = _ctx_end(self.context.copy())
        
        res = {}
        res_activo = {}
        res_pasivo = {}
        res_capital = {}
        res_pasivo_capital = {}
        res_total_result = {}
        res_state_finance = {}
        result_acc = []       
        name_account_mayor = ""

        total_activo_init = 0.0
        total_activo_debit = 0.0
        total_activo_credit = 0.0
        total_activo_ytd = 0.0
        total_activo_balance = 0.0

        total_pasivo_init = 0.0
        total_pasivo_debit = 0.0
        total_pasivo_credit = 0.0
        total_pasivo_ytd = 0.0
        total_pasivo_balance = 0.0

        total_capital_init = 0.0
        total_capital_debit = 0.0
        total_capital_credit = 0.0
        total_capital_ytd = 0.0
        total_capital_balance = 0.0

        total_ingreso_init = 0.0
        total_ingreso_debit = 0.0
        total_ingreso_credit = 0.0
        total_ingreso_ytd = 0.0
        total_ingreso_balance = 0.0

        change_account_mayor = 0
        cont = 0

        # archi_text = ""
        # archi=open('/home/equihua/balance.txt','w')
        # archi.close()

        for aa_id in account_ids:
            id = aa_id[0]
            #pdb.set_trace()
            #
            # Check if we need to include this level
            #
            if not form['display_account_level'] or aa_id[3].level <= form['display_account_level']:
                if aa_id[3].level == 1:
                    if cont > 1:
                        if change_account_mayor == 1:
                            result_acc.append(res_activo)
                            #change_account_mayor = 1
                        elif change_account_mayor == 2:
                            result_acc.append(res_pasivo)
                            #change_account_mayor = 2

                res = {
                    'id'        : id,
                    'type'      : aa_id[3].type,
                    'code'      : aa_id[3].code,
                    'name'      : (aa_id[2] and not aa_id[1]) and 'TOTAL %s'%(aa_id[3].name.upper()) or aa_id[3].name,
                    'parent_id' : aa_id[3].parent_id and aa_id[3].parent_id.id,
                    'level'     : aa_id[3].level,
                    'account_category': aa_id[3].account_category,
                    #'label'     : aa_id[1],
                    #'total'     : aa_id[2],
                    'change_sign' : credit_account_ids and (id  in credit_account_ids and -1 or 1) or 1
                }
                
                aa_brw_init = account_obj.browse(self.cr, self.uid, id, ctx_init)
                aa_brw_end  = account_obj.browse(self.cr, self.uid, id, ctx_end)

                i,d,c = map(z,[aa_brw_init.balance,aa_brw_end.debit,aa_brw_end.credit])
                b = z(i+d-c)
                res.update({
                    'balanceinit': abs(self.exchange(i)),
                    'debit': abs(self.exchange(d)),
                    'credit': abs(self.exchange(c)),
                    'ytd': abs(self.exchange(d-c)),
                })

                res.update({
                    'balance': abs(self.exchange(b)),
                })

                #
                # Check whether we must include this line in the report or not
                #
                to_include = False
                
                if form['display_account'] == 'mov' and aa_id[3].parent_id:
                    # Include accounts with movements
                    if abs(d) >= 0.005 or abs(c) >= 0.005:
                        to_include = True
                elif form['display_account'] == 'bal' and aa_id[3].parent_id:
                    # Include accounts with balance
                    if abs(b) >= 0.005:
                        to_include = True
                elif form['display_account'] == 'bal_mov' and aa_id[3].parent_id:
                        # Include accounts with balance or movements
                    if abs(b) >= 0.005 or abs(d) >= 0.005 or abs(c) >= 0.005:
                        to_include = True
                else:
                    # Include all accounts
                    to_include = True
                
                #if to_include and aa_id[3].type == 'view' and aa_id[3].level:
                if to_include:
                    result_acc.append(res)
                    #ACTIVO
                    if res['account_category'] == 'asset':
                        total_activo_init = res['balanceinit']
                        total_activo_debit = res['debit']
                        total_activo_credit = res['credit']
                        total_activo_ytd = res['ytd']
                        total_activo_balance = res['balance']

                        res_activo = {
                            'id':0,
                            'type' : 'view',
                            'code':'',
                            'name': 'TOTAL ACTIVO ',
                            'parent_id':0,
                            'level': 1,
                            'change_sign':1,
                            'balanceinit': total_activo_init,
                            'debit': total_activo_debit,
                            'credit': total_activo_credit,
                            'ytd': total_activo_ytd,
                            'balance': total_activo_balance,
                        }
                        change_account_mayor = 1

                    #PASIVO
                    elif res['account_category'] == 'liability':
                        total_pasivo_init = res['balanceinit']
                        total_pasivo_debit = res['debit']
                        total_pasivo_credit = res['credit']
                        total_pasivo_ytd = res['ytd']
                        total_pasivo_balance = res['balance']

                        res_pasivo = {
                            'id':0,
                            'type' : 'view',
                            'code':'',
                            'name': 'TOTAL PASIVO ',
                            'parent_id':0,
                            'level': 1,
                            'change_sign':1,
                            'balanceinit': total_pasivo_init,
                            'debit': total_pasivo_debit,
                            'credit': total_pasivo_credit,
                            'ytd': total_pasivo_ytd,
                            'balance': total_pasivo_balance,
                        }
                        change_account_mayor = 2
                    #CAPITAL
                    #elif res['account_category'] == 'equity':
                    elif res['type'] == 'view' and res['code'][:1] == '3' and res['account_category'] == 'balance_sheet':
                        total_capital_init += res['balanceinit']
                        total_capital_debit += res['debit']
                        total_capital_credit += res['credit']
                        total_capital_ytd += res['ytd']
                        total_capital_balance += res['balance']

                        res_capital = {
                            'id':0,
                            'type' : 'view',
                            'code':'',
                            'name': 'TOTAL CAPITAL ',
                            'parent_id':0,
                            'level': 1,
                            'change_sign':1,
                            'balanceinit': total_capital_init,
                            'debit': total_capital_debit,
                            'credit': total_capital_credit,
                            'ytd': total_capital_ytd,
                            'balance': total_capital_balance,
                        }
                    elif res['account_category'] == 'income':
                        total_ingreso_init = res['balanceinit']
                        total_ingreso_debit = res['debit']
                        total_ingreso_credit = res['credit']
                        total_ingreso_ytd = res['ytd']
                        total_ingreso_balance = res['balance']

                        total_capital_init = abs(total_capital_init - total_ingreso_init)
                        total_capital_debit = abs(total_capital_debit - total_ingreso_debit)
                        total_capital_credit = abs(total_capital_credit - total_ingreso_credit)
                        total_capital_ytd = abs(total_capital_ytd - total_ingreso_ytd)
                        total_capital_balance = abs(total_capital_balance - total_ingreso_balance)

                        res_capital = {
                            'id':0,
                            'type' : 'view',
                            'code':'',
                            'name': 'TOTAL CAPITAL ',
                            'parent_id':0,
                            'level': 1,
                            'change_sign':1,
                            'balanceinit': total_capital_init,
                            'debit': total_capital_debit,
                            'credit': total_capital_credit,
                            'ytd': total_capital_ytd,
                            'balance': total_capital_balance,
                            }
                cont += 1
                #print str(res['code']) + '\t' + str(res['name']) + '\t' + str(res['balanceinit']) + '\t' + str(res['debit']) + '\t' + str(res['credit']) + '\t' + str(res['ytd']) + '\t' + str(res['balance']) + '\t' + str(res['type']) + '\n' 

        res_pasivo_capital = {
                'id':0,
                'type' : 'view',
                'code':'',
                'name': 'TOTAL PASIVO + CAPITAL ',
                'parent_id':0,
                'level': 1,
                'change_sign':1,
                'balanceinit': abs(total_pasivo_init + total_capital_init),
                'debit': abs(total_pasivo_debit + total_capital_debit),
                'credit': abs(total_pasivo_credit + total_capital_credit),
                'ytd': abs(total_pasivo_ytd + total_capital_ytd),
                'balance': abs(total_pasivo_balance + total_capital_balance),
                }

        res_state_finance = {
                'id':0,
                'type' : 'view',
                'code':'',
                'name': 'ESTADO DE POSICION FINANCIERA ',
                'parent_id':0,
                'level': 1,
                'change_sign':1,
                'balanceinit': abs(total_activo_init - (total_pasivo_init + total_capital_init)),
                'debit': abs(total_activo_debit + total_pasivo_debit + total_capital_debit),
                'credit': abs(total_activo_credit + total_pasivo_credit + total_capital_credit),
                'ytd': abs(total_activo_ytd - (total_pasivo_ytd + total_capital_ytd)),
                'balance': abs(total_activo_balance - (total_pasivo_balance + total_capital_balance)),
                }

        # archi_text += str(res_capital['code']) + '\t' + str(res_capital['name']) + '\t' + str(res_capital['balanceinit']) + '\t' + str(res_capital['debit']) + '\t' + str(res_capital['credit']) + '\t' + str(res_capital['ytd']) + '\t' + str(res_capital['balance']) + '\t' + str(res_capital['type']) + '\t' + str(res_capital['type']) + '\n'
        # archi=open('/home/equihua/balance.txt','w')
        # archi.write(archi_text)
        # archi.close()

        result_acc.append(res_capital)
        result_acc.append(res_pasivo_capital)
        #result_acc.append(res_state_finance)
        #print result_acc
        return result_acc
                       
# report_sxw.report_sxw('report.balance.sheet', 
#                       'wizard.balance.sheet', 
#                       'reports_account/report/balance_full_5_cols.rml',
#                        parser=balance_sheet_parser, 
#                        header=False)

report_sxw.report_sxw('report.balance.sheet.mako', 
                      'wizard.balance.sheet', 
                      'reports_account/report/balance_sheet_report.mako',
                       parser=balance_sheet_parser, 
                       header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: