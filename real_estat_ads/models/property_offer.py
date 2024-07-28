from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estat.property.offer"
    _description = "Estat Property Offer"

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f'{rec.property_id.name}-{rec.partner_id.name}'
            else:
                rec.name = False

    name = fields.Char(string="Name", compute=_compute_name)
    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')],
                              string="Status")
    partner_id = fields.Many2one('res.partner', string="Costumer")
    property_id = fields.Many2one('estat.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    # _sql_constraints = [
    #    ('check_validity', 'check(validity>0)', 'deadline must be greader than create_date')
    # ]

    # @api.model
    # def _set_create_date(self):
    #   return fields.Date.today()

    create_date = fields.Date(string="Create_date")

    @api.depends('create_date', 'validity')
    # @api.depends_context()
    def _compute_deadline(self):
        # print(self.env.context)
        # print(self._context)
        for rec in self:
            if rec.create_date and rec.validity:
                rec.deadline = rec.create_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.create_date and rec.deadline:
                rec.validity = (rec.deadline - rec.create_date).days
            else:
                rec.validity = False

        # @api.autovacuum
        # def _clean_offers(self):
        #    self.search([('status', '=', 'refused')]).unlink()

    # ORM methode
    @api.model_create_multi
    def _create(self, vals):
        for rec in vals:
            if not rec.get('create_date'):
                rec['create_date'] = fields.Date.today()
        return super(PropertyOffer, self)._create(vals)

    # ORM methode

    # def _write(self, vals):
    #   print(vals)
    #  res_partner_ids = self.env['res.partner'].search_count([
    #     ('is_company', '=', True)
    # ])
    # print(res_partner_ids)
    # return super(PropertyOffer, self)._write(vals)

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline and rec.create_date:
                if rec.deadline <= rec.create_date:
                    raise ValidationError(_('deadline must be greader than create_date'))

    def action_accept_offer(self):
        if self.property_id:
            self._validation_accepted_offer()
            # self.property_id.write({ ==> ORM methode like self.env.write()
            #    'selling_price': self.price
            # })
            self.property_id.selling_price = self.price
            self.property_id.state = 'accepted'

        self.status = "accepted"

    def _validation_accepted_offer(self):
        offer_ids = self.env['estat.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if offer_ids:
            raise ValidationError("You have an accepted offer already")

    def action_cancel_offer(self):
        self.status = "refused"
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.selling_price = 0
            self.property_id.state = 'received'

    # abstract,transient,regular module

    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids', [])
        if active_ids:
            offer_ids = self.env['estat.property.offer'].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10

