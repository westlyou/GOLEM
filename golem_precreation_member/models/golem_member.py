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

""" GOLEM Members """

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
_LOGGER = logging.getLogger(__name__)


class GolemMember(models.Model):
    """ GOLEM Member model """
    _inherit = 'golem.member'

    @api.multi
    def precreation_search(self):
        self.ensure_one()
        return {'name' : _('Please enter the rejection reason'),
                'type' : 'ir.actions.act_window',
                'res_model' : 'golem.precreation.member.wizard',
                #'context': {'default_reservation_id': reservation_id.id},
                'view_mode': 'form',
                'target': 'new'}
