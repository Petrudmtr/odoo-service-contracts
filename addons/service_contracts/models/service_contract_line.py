from odoo import models, fields, api


class ServiceContractLine(models.Model):
    _name = 'service.contract.line'
    _description = 'Service Contract Line'

    contract_id = fields.Many2one('service.contract', string='Contract', required=True, ondelete='cascade')
    name = fields.Char(string='Service Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price_unit
