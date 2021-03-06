# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class account_financial_report(osv.osv):
    
    _inherit = "afr"
    _description = """Add a new many2many field related to model account.cost.center"""
    _columns = {
                "cost_center_ids": fields.many2many("account.cost.center", "afr_cost_center",
                                                    "cost_center_id", "afr_id", "Cost Centers")
               }

account_financial_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: