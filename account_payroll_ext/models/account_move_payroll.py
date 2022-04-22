# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

class AccountMovePayroll(models.Model):
    _name = 'account.move.payroll'
    _inherit = 'mail.thread'
    _description = 'Account move payroll'

    name = fields.Char(
        string="Name",
        compute="_concatenate_name")
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee")
    employee_name = fields.Char(
        string="Employee name",
        related="employee_id.name")
    concatenate_name = fields.Char(
        string="Concatenate")
    code = fields.Char(
        string="Code",
        default="New",
        readonly=True,
        copy=False)
    project_id = fields.Many2one(
        'bim.project',
        string="Project BIM")


    @api.onchange('name')
    def _upper_name(self):
    # Función para colocar en mayusculas       
        self.name = self.name.upper() if self.name else False


    def generate_records_account_move(self):
    # Función generar asientos contables
        print('Testing...!')


    @api.model
    def create(self, vals):
        # Función para heredar create y agregar secuencia automatica
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('amp')
        result = super(AccountMovePayroll, self).create(vals)

        return result


    @api.depends('code','employee_name','employee_id')
    def _concatenate_name(self):
       # Concatenar campos
        self.name = "%s %s" % (
            self.code if self.code else "",
            self.employee_name if self.employee_name else "")
