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

from odoo import models, fields, api, _

class GolemMember(models.Model):
    """ GOLEM Member adaptations """
    _inherit = 'golem.member'

    #ajout d'un champs O2M vers member_id de golem.activity.queue
    activity_queue_ids = fields.One2many('golem.activity.queue',
                                         'member_id', 'Pending registration')

    #verifier si nombre d'inscription sur activité est supérieur au place disponible
    @api.multi
    @api.onchange('activity_registration_ids')
    def _checkRegistrationNumber(self):
        self.ensure_one()
        member_id = self[0]

        for registration in member_id.activity_registration_ids:
            activity = registration.activity_id
            if len(activity.activity_registration_ids) > activity.places and activity.queue_allowed:
                warning_message = _('This activity : {} is already full, please'
                                    ' discard changes and register in'
                                    ' the queue using the bellow button')
                return {
                    'warning' : {
                        'title' : _('Warning'),
                        'message': warning_message.format(activity.name),
                    }
                }

    #lancer popup pour choisir activité à s'inscrire
    @api.multi
    def choose_queue_to_register(self):
        print "_________________________________________________"
        print self
        self.ensure_one()
        member_id = self[0]

        return {
            'name'      : _('Choose the activity to register in'),
            'type'      : 'ir.actions.act_window',
            'res_model' : 'golem.activity.queue.choose.wizard',
            'view_mode': 'form',
            'context' : {'default_member_id' : member_id.id},
            'target': 'new',
        }
