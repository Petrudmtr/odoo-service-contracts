from odoo import models, fields, api


class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date_open desc'

    name = fields.Char(string='Request Title', required=True, tracking=True)
    contract_id = fields.Many2one('service.contract', string='Contract', required=True)
    partner_id = fields.Many2one(related='contract_id.partner_id', string='Customer', store=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='0')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='new', tracking=True)
    description = fields.Text(string='Description')
    date_open = fields.Datetime(string='Opened On', default=fields.Datetime.now)
    date_closed = fields.Datetime(string='Closed On')

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done', 'date_closed': fields.Datetime.now()})

    def action_cancel(self):
        self.write({'state': 'cancelled', 'date_closed': fields.Datetime.now()})
