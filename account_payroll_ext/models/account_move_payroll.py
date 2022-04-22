# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountMovePayroll(models.Model):
    _name = 'account.move.payroll'
    _inherit = 'mail.thread'
    _description = 'Account move payroll'

    name = fields.Char(string="Name")
