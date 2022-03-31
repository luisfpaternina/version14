# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleTypeService(models.Model):
    _name = 'sale.type.service'
    _inherit = 'mail.thread'
    _description = 'Sale type service'

    name = fields.Char(
        string="Name")
    item = fields.Integer()
    code = fields.Char(
        string="Code")
    active = fields.Boolean(
        string="Active",
        default=True)
    order_id = fields.Many2one(
        'sale.order',
        string="Sale Order")
    suscription_id = fields.Many2one(
        'sale.subscription',
        string="Suscription")
    type_description = fields.Text(
        string="Description")


    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False
