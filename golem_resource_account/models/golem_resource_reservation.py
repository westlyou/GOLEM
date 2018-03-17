# -*- coding: utf-8 -*-

#    Copyright 2018 Youssef El Ouahby <youssef@yaltik.com>
#    Copyright 2018 Fabien Bourgeois <fabien@yaltik.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" GOLEM Resource Reservation  Adaptation"""


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class GolemResourceReservation(models.Model):
    """ GOLEM Resource Reservation Adaptation """
    _inherit = 'golem.resource.reservation'

    invoice_id = fields.Many2one('account.invoice')
    invoicing_state = fields.Char(compute="_compute_invoicing_state",
                                  search='_search_invoicing_state',
                                  string="Invoicing Status",
                                  default="None")

    def _search_invoicing_state(self, operator, value):
        if value == "None":
            reservation = self.env['golem.resource.reservation'].search([('invoice_id', '=', False)])
            return [('id', 'in', reservation.mapped('id'))]
        else:
            return [('invoice_id.state', operator, value)]
        

        """
        print '________________________________'
        print("kelri")

        if self.invoice_id:
            invoicing_state = self.invoice_id.state
            print "_____________________1"
            print invoicing_state
            return [('invoicing_state', operator, value)]
        else:
            invoicing_state = "None"
            print '_____________________2'
            print invoicing_state
            return [('invoicing_state', operator, value)]
            print invoicing_state
        """
    @api.multi
    @api.depends('invoice_id')
    def _compute_invoicing_state(self):
        """ Compute invoicing_state """
        for reservation in self:
            if reservation.invoice_id:
                reservation.invoicing_state = reservation.invoice_id.state
            else:
                reservation.invoicing_state = "None"


    @api.multi
    def create_invoice(self):
        for reservation in self:
            inv_obj = self.env['account.invoice']
            partner_id = reservation.partner_id
            product = reservation.resource_id.product_tmpl_id
            amount = product.standard_price
            quantity = reservation.hour_stop - reservation.hour_start
            if product.id:
                account_id = product.property_account_income_id.id

            if not account_id:
                account_id = product.categ_id.property_account_income_categ_id.id

            if not account_id:
                raise UserError(
                    _('There is no income account defined for this product: "%s". \
                       You may have to install a chart of account from Accounting \
                       app, settings menu.') % (product.name,))


            reservation.invoice_id = inv_obj.create({
                'name': reservation.name,
                #'origin': self.application_number,
                'type': 'out_invoice',
                'reference': False,
                'account_id': partner_id.property_account_receivable_id.id,
                'partner_id': partner_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': reservation.resource_id.name,
                    #'origin': ,
                    'account_id': account_id,
                    'price_unit': amount,
                    'quantity': quantity,
                    'discount': 0.0,
                    'uom_id': product.uom_id.id,
                    'product_id': product.id,
                    })],
                })
