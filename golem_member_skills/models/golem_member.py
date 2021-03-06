# -*- coding: utf-8 -*-

#    Copyright 2017 Fabien Bourgeois <fabien@yaltik.com>
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

""" GOLEM Member Skills """

from odoo import models, fields


class ResPartner(models.Model):
    """ Partner adaptations """
    _inherit = 'res.partner'

    is_volunteer = fields.Boolean('Volunteer?')
    skill_ids = fields.Many2many('golem.member.skill', string='Skills',
                                 index=True)


class GolemMemberSkill(models.Model):
    """ Member adaptations """
    _name = 'golem.member.skill'
    _description = 'GOLEM Member Skill'

    _sql_constraints = [('golem_member_skill_name_uniq', 'UNIQUE (name)',
                         'Member skill must be unique.')]

    name = fields.Char('Skill', required=True, index=True)
