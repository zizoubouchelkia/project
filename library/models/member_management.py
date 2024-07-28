from odoo import fields, models, api


class Member(models.Model):
    _name = 'library.member'
    _description = 'library member'

    name = fields.Char(string='Name', required=True)
    membership_id = fields.Char(string='Membership ID', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    adresse = fields.Text('Address')
    membership_type = fields.Selection([
        ('regular', 'Regular'),
        ('premium', 'Premium')
    ], string='Membership Type', default='regular')

