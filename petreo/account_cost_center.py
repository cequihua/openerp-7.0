from osv import fields, osv

class account_cost_center(osv.osv):
    _name = 'petreo.account.cost.center'
    _columns = {
                "name": fields.char("Name", size=64, required=True),
                }