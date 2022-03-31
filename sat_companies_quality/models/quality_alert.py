from odoo import models, fields, api, _
from datetime import datetime, date
import logging


class QualityAlert(models.Model):
    _inherit = 'quality.alert'