from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="age", compute="_compute_age_author")
    age_label = fields.Char(string="Age", compute="_compute_age_label")
    biography = fields.Text(string="Biography")
    book_ids = fields.One2many('library.book', 'author_id', string="Books")
    cover_image_author = fields.Binary(string='Cover Image Author')
    date_of_birth = fields.Date(string='Date of Birth')
    nationality = fields.Char(string='Nationality')
    awards = fields.Text(string='Awards')
    website = fields.Char(string='Website')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')

    @api.depends("date_of_birth")
    def _compute_age_author(self):
        for author in self:
            if author.date_of_birth:
                author.age = date.today().year - author.date_of_birth.year
            else:
                author.age = 0

    @api.depends("age")
    def _compute_age_label(self):
        for book in self:
            if book.age == 1:
                book.age_label = f"{book.age} year"
            elif book.age > 1:
                book.age_label = f"{book.age} years"
            elif book.age == 0:
                book.age_label = 0
            else:
                raise ValidationError("Age must be positive")
