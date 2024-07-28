from odoo import models, fields, api, _


class Property(models.Model):
    _name = "estat.property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Estat Properties"

    name = fields.Char(string="Name")
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel')
    ], default='new', string='status')
    type_id = fields.Many2one('estat.property.type', string="Property Type")
    tag_ids = fields.Many2many('estat.property.tag', string="Property Tag")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", tracking=True)
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')],
                                          string="Garden Orientation", default='north')
    offer_ids = fields.One2many('estat.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    phone = fields.Char(string="phone", related="buyer_id.function")

    @api.depends('living_area', 'garden_area')
    def compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string="Total_Area", compute=compute_total_area)

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    # def action_testing_client(self):
    #    return {
    #       'type': 'ir.actions.client',
    # 'tag': 'reload'
    # 'tag': 'apps'
    #      'tag': 'display_notification',
    #     'params': {
    #        'title': _('testing client'),
    #       'type': 'warning',
    #      'sticky': False
    # }
    # }

    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://odoo.com',
            'target': 'new',
        }

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'estat_property - %s' % self.name


class PropertyType(models.Model):
    _name = "estat.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name")


class PropertyTag(models.Model):
    _name = "estat.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")
