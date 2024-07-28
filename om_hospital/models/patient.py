from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Hospitalpatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "patient records"

    name = fields.Char(string='name', required=True, tracking=True)
    age = fields.Integer(string="age", tracking=True)
    is_child = fields.Boolean(string="is child ?", tracking=True)
    notes = fields.Text(string="notes", tracking=True)
    gender = fields.Selection([('Male', 'male'), ('Female', 'female'), ('Others', 'others')], tracking=True,
                              string="gender")
    Capitelaz_Name = fields.Char(string='Capitelaz_Name', compute='_compute_Capitelaz_Name', store=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    doctor_id = fields.Many2one('hospital.doctor', string='doctor')
    tag_ids = fields.Many2many('res.partner.category', 'hospital_patient_tag_rel', 'patient_id', 'tag_id',
                               string="tags")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('Hospital.patient')
        return super(Hospitalpatient, self).create(vals_list)

    @api.constrains('is_child', 'age')
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age == 0:
                raise ValidationError(_('age has to be recorded !'))

    @api.depends('name')
    def _compute_Capitelaz_Name(self):
        for rec in self:
            if rec.name:
                rec.Capitelaz_Name = rec.name.upper()
            else:
                rec.Capitelaz_Name = ''

    @api.onchange('age')
    def on_change_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False
