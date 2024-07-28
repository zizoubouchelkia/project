from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = "library.book"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Book"

    name = fields.Char(string="Title", required=True, tracking=True)
    author_id = fields.Many2one('library.author', string='Author', tracking=True)
    isbn = fields.Char(string='ISBN', tracking=True)
    publication_date = fields.Date(string="Publication Date", tracking=True)
    publisher = fields.Many2one('library.publisher', string="Publisher", tracking=True)
    genre_ids = fields.Many2many('library.book.topic', string="Topic")
    copy_count = fields.Integer(string="Number of Copies", default=1, tracking=True)
    pages = fields.Integer(string='Number of Pages')
    language = fields.Selection([
        ('english', 'English'),
        ('french', 'French'),
        ('spanish', 'Spanish'),
        ('german', 'German'),
        ('other', 'Other')
    ], string='Language')
    other_language = fields.Char(string="Other language")
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost')
    ], string='Status', default='available')
    cover_image = fields.Binary(string='Cover Image')
    price = fields.Float(string='Price', tracking=True)
    location = fields.Char(string='Location')
    age = fields.Integer(string='Book Age', compute='_compute_age', store=True)
    borrow_ids = fields.One2many('library.borrow', 'book_id', string='Borrow Records')
    times_borrowed = fields.Integer(string='Times Borrowed', compute='_compute_times_borrowed')
    age_label = fields.Char(string='Age Label', compute='_compute_age_label', store=True)

    @api.depends('publication_date')
    def _compute_age(self):
        for book in self:
            if book.publication_date:
                book.age = date.today().year - book.publication_date.year
            else:
                book.age = 0

    @api.depends('age')
    def _compute_age_label(self):
        for book in self:
            if book.age == 1:
                book.age_label = f"{book.age} year"
            elif book.age > 1:
                book.age_label = f"{book.age} years"
            else:
                book.age_label = 0


    @api.depends('borrow_ids')
    def _compute_times_borrowed(self):
        for book in self:
            book.times_borrowed = len(book.borrow_ids)

    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN must be unique.')
    ]

    @api.constrains('price', 'pages')
    def _check_positive_values(self):
        for book in self:
            if book.pages < 0 or book.price < 0:
                raise ValidationError('Price and Pages must be positive values.')

    def action_reserved(self):
        self.status = 'reserved'

    def action_lost(self):
        self.status = 'lost'


class Topic(models.Model):
    _name = "library.book.topic"
    _description = "Library Book Topic"

    name = fields.Char(string="Topic")
    color = fields.Integer(string="Color")
