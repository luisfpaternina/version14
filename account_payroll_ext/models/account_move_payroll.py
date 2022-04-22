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
    state = fields.Selection([
        ('draft','Draft'),
        ('done','Done')],string="State",default="draft")
    mjs = fields.Char(
        string="Mjs",
        compute="_compute_mjs")
    is_done = fields.Boolean(
        string="Is done",
        compute="_compute_mjs")


    @api.depends('state')
    def _compute_mjs(self):
        for record in self:
            if record.state == 'done':
                record.mjs = 'Accounting entries have been created!'
                record.is_done = True
            else:
                record.mjs = ' '
                record.is_done = False


    def generate_records_account_move(self):
    # Función generar asientos contables y cambio de estado a hecho
        for record in self:
            record.write({'state': 'done'})
            record.get_records_attendance()
            print('Testing')


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
       for record in self:
            record.name = "[%s]%s" % (
                record.code if record.code else "",
                record.employee_name if record.employee_name else "")


    def get_records_attendance(self):
        for record in self:
            attendance_obj = record.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('project_id', '=', record.project_id.id)])
            if attendance_obj:
                print('entro')
                logging.info(attendance_obj)

