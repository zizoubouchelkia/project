from odoo import fields, models, api
from odoo.exceptions import ValidationError


class LibraryBorrow(models.Model):
    _name = "library.borrow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Library Borrow Record"


    book_id = fields.Many2one('library.book', string="Book", required=True)
    member_id = fields.Many2one('library.member', string="Member", required=True)
    borrow_date = fields.Date('Borrow Date', default=fields.Date.today)
    return_date = fields.Date('Return Date')
    days_count = fields.Integer('borrowing_days', compute="_limite_date")
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned')
    ], string='Status', default='borrowed')

    @api.depends("return_date", "borrow_date")
    def _limite_date(self):
        for book in self:
            if book.borrow_date and book.return_date:
                borrow_date = fields.Date.from_string(book.borrow_date)
                return_date = fields.Date.from_string(book.return_date)
                book.days_count = (return_date - borrow_date).days
            else:
                book.days_count = 0
        if self.days_count < 0:
            raise ValidationError("Days Must Be positive !!!!!!!!")
        elif self.days_count > 25:
            raise ValidationError("You Can Borrow For 25 Days Maximum !!!!!")

    def action_borrowed(self):
        self.state = "borrowed"

    def action_returned(self):
        self.state = "returned"
