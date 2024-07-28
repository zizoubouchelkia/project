from odoo import models, fields

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Library Publisher'

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address')
    contact = fields.Char(string='Contact Information')