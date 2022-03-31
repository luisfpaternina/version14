# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import base64
import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    address = fields.Char(
        string="Address",
        related="partner_id.street",
        tracking=True)
    population_id = fields.Many2one(
        'res.partner.population',
        string="Population",
        tracking=True)
    sale_type = fields.Selection([
        ('maintenance','Maintenance'),
        ('mounting','Mounting'),
        ('repair','Repair')],string="Sale type")
    type_contract = fields.Selection([
        ('normal','Normal'),
        ('risk','All risk')],string="Contract type")
    is_create_task = fields.Boolean(
        string="Create task",
        tracking=True,
        related="sale_type_id.is_create_task")
    check_contract_type = fields.Boolean(
        compute="_compute_check_contract_type",
        )
    type_service_id = fields.One2many(
        'sale.check.type.contract',
        'order_id',
        string='Type service'
        )
    pdf_file_sale_contract = fields.Binary(
        compute="action_get_attachment")
    signature_url_text = fields.Text(
        string="Signature URL")
    check_signature = fields.Boolean(
        string="Check signature")
    is_forecast_made = fields.Boolean(  
        string="Forecast Made")
    product_id = fields.Many2one(
        'product.template',
        string='Gadget')
    task_user_id = fields.Many2one(
        'res.users',
        'Task User id')
    check_product = fields.Boolean(
        compute='compute_check_product')
    date_begin = fields.Datetime(
        string="Date begin")
    date_end = fields.Datetime(
        string="Date end")
    quote_date_sent = fields.Date(
        string="Quote date sent",
        compute="_calculated_quote_date_sent")
    quote_date_sent_min = fields.Date(
        string="Quote date sent min")
    rae = fields.Char(
        string="R.A.E",
        related="product_id.rae")
    contract_send = fields.Boolean()
    pdf_description = fields.Char(
        string="PDF description",
        tracking=True)
    is_pdf_true = fields.Boolean(
        string="PDF True")
    udn_id = fields.Many2one(
        'project.task.categ.udn',
        string="Udn")
    is_maintenance = fields.Boolean(
        string="Is maintenance")
    is_line = fields.Boolean(
        string="Is line")
    is_other = fields.Boolean(
        string="Other")
    is_mounting = fields.Boolean(
        string="Is mounting")
    is_normative = fields.Boolean(
        string="Normative",
        related="udn_id.is_normative")
    normative_date = fields.Date(
        string="Normative date")


    @api.onchange('sale_type_id')
    def domain_saletype_udn(self):
        for record in self:
            if record.sale_type_id:
                return {'domain': {'udn_id': [('ot_type_id', '=', record.sale_type_id.id)]}}
            else:
                return {'domain': {'udn_id': []}}


    @api.onchange('state','name')
    def send_pdf_description(self):
        for record in self:
            if record.pdf_file_sale_contract:
                record.pdf_description = 'CONTRATO HA SIDO FIRMADO'


    @api.onchange('product_id')
    def onchange_check_product(self):
        for record in self:
            if record.product_id.employee_notice_id.user_id:
                record.task_user_id = record.product_id.employee_notice_id.user_id
            sale_type = record.product_id.subscription_template_id.sale_type_id
            gadgets_contract = record.product_id.subscription_template_id.gadgets_contract_type_id
            record.sale_type_id = sale_type
            record.gadgets_contract_type_id = gadgets_contract


    @api.depends('product_id')
    def compute_check_product(self):
        for record in self:
            if record.product_id:
                record.check_product=True
            else:
                record.check_product=False
        

    @api.depends('sale_type_id')
    def _compute_check_contract_type(self):
        for record in self:
            record.type_contract = False
            if record.sale_type_id.code == '01':
                record.check_contract_type = True
            else:
                record.check_contract_type = False


    @api.constrains('contract_line_ids')
    def _check_exist_record_in_lines(self):
        for rec in self:
            exis_record_lines = []
            for line in rec.contract_line_ids:
                if line.contact_id.id in exis_record_lines:
                    raise ValidationError(_(
                        'The item should be one per line'))
                exis_record_lines.append(line.contact_id.id)


    @api.onchange('type_service_id')
    def get_item_count(self):
        for rec in self:
            count = 1
            for line in rec.type_service_id:
                line.item = count
                count += 1


    def get_table_type_contracts(self):

        flag = False
        table = '<ul>'
        for  type_service_id in self.type_service_id:
            flag = True
            table += '<li>' + str(type_service_id.type_service_id.name) + '  </li>'
        
        table += '</ul>'
        return table if flag else False
    

    def action_contract_send(self):
        self.contract_send = True
        self.ensure_one()
        template = self.env.ref('sat_companies_sale.email_contract_signature')
        lang = self.env.context.get('lang')
        template_id = template.id
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    def _compute_file_sale_contract(self):
        pdf = self.env.ref('sat_companies_sale.action_email_contract_signature').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])


    @api.depends('check_signature')
    def action_get_attachment(self):
        for record in self:
            if record.check_signature == True:
                pdf = self.env.ref('sat_companies_sale.action_email_contract_signature')._render_qweb_pdf(self.ids)
                print(pdf)
                b64_pdf = base64.b64encode(pdf[0])
                record.pdf_file_sale_contract = b64_pdf
                if record.order_line:
                    for line in record.order_line:
                        line.subscription_id.pdf_file_sale_contract = record.pdf_file_sale_contract 
            else:
                record.pdf_file_sale_contract = False


    @api.depends('state')
    def _calculated_quote_date_sent(self):
        today = date.today()
        for record in self:
            if record.state == 'sent':
                record.quote_date_sent = today
            else:
                print("Presupuestos sin enviar...!")
                record.quote_date_sent = False


    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
            ir_model_data.get_object_reference('test_email', 'email_template_contract_suspension')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
        'default_model': 'sale.order',
        'default_res_id': self.ids[0],
        'default_use_template': bool(template_id),
        'default_template_id': template_id,
        'default_composition_mode': 'comment',
        }
        return {
        'name': _('Compose Email'),
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id, 'form')],
        'view_id': compose_form_id,
        'target': 'new',
        'context': ctx,
        }
