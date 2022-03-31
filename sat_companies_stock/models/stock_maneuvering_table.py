# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockManeuveringTable(models.Model):
    _name = 'stock.maneuvering.table'
    _inherit = 'mail.thread'
    _description = 'Maneuvering table'

    name = fields.Char(
        string="Name",
        tracking=True)
    active = fields.Boolean(
        string="Active",
        tracking=True,
        default=True)

    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False
