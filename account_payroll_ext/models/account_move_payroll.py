# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountMovePayroll(models.Model):
    _name = 'account.move.payroll'
    _inherit = 'mail.thread'
    _description = 'Account move payroll'

    name = fields.Char(
        string="Name")
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee")
    employee_name = fields.Char(
        string="Employee name",
        related="employee_id.name")
    concatenate_name = fields.Char(
        string="Concatenate")
