from odoo import api, models, fields, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = "mail.thread"
    _description = "Hospital Doctor"

    name = fields.Char(string='Name', required=True, tracking=True)
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], tracking=True,
                              string="Gender")
    ref = fields.Char(string='Reference', required=True)
    active = fields.Boolean(default=True)

    def name_get(self):
        res = []
        for rec in self:
            name = f'{rec.name} - {rec.ref}'
            res.append((rec.id, name))
        return res
