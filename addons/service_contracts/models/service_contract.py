from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class ServiceContract(models.Model):
    _name = 'service.contract'
    _description = 'Service Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end asc, name'

    name = fields.Char(string='Contract Number', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('service.contract.line', 'contract_id', string='Services')
    request_ids = fields.One2many('service.request', 'contract_id', string='Requests')
    total_value = fields.Float(string='Total Value', compute='_compute_total_value', store=True)
    days_remaining = fields.Integer(string='Days Remaining', compute='_compute_days_remaining')
    notes = fields.Text(string='Notes')
    reminder_sent = fields.Boolean(string='Reminder Sent', default=False)

    @api.depends('line_ids.subtotal')
    def _compute_total_value(self):
        for rec in self:
            rec.total_value = sum(rec.line_ids.mapped('subtotal'))

    @api.depends('date_end')
    def _compute_days_remaining(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_end:
                rec.days_remaining = (rec.date_end - today).days
            else:
                rec.days_remaining = 0

    def action_activate(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def action_send_expiry_reminder(self):
        template = self.env.ref('service_contracts.mail_template_contract_expiry', raise_if_not_found=False)
        if template:
            for contract in self:
                template.send_mail(contract.id, force_send=True)

    @api.model
    def _cron_check_contract_expiry(self):
        today = fields.Date.today()

        # Mark active contracts as expired if end date has passed
        expired = self.search([('state', '=', 'active'), ('date_end', '<', today)])
        expired.write({'state': 'expired'})

        # Send reminder once for contracts expiring within 30 days
        remind_date = today + relativedelta(days=30)
        expiring_soon = self.search([
            ('state', '=', 'active'),
            ('reminder_sent', '=', False),
            ('date_end', '>=', today),
            ('date_end', '<=', remind_date),
        ])
        template = self.env.ref('service_contracts.mail_template_contract_expiry', raise_if_not_found=False)
        if template:
            for contract in expiring_soon:
                template.send_mail(contract.id, force_send=False)
            expiring_soon.write({'reminder_sent': True})
