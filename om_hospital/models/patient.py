
from odoo import api, fields, models, _

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Details"

    image = fields.Binary(string='Patient Image')
    referance = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                            default=lambda self: _('Om_hospital'))
    name = fields.Char(string='Name', required=True, tracking=True)
    responsible = fields.Many2one(string="Responsible", comodel_name='res.partner')
    age = fields.Integer(string='Age', tracking=True)
    birthdate = fields.Date(string='Birth Date', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    referred = fields.Many2one('hospital.doctor', string="Referred to", required=True)

    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                             ('done', 'Done'), ('cancel', 'cancelled')], default="draft", string="States", tracking=True)
    appointment_count = fields.Integer(string='Total Appointments', compute='compute_appointment_count')
#action to calculate total appointment
    def compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count
#action for butoons
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
#to set default value in any field
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
#to assign sequence inplace of default set value
        if vals.get('referance', _('Om_hospital')) == _('Om_hospital'):
            vals['referance'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('Om_hospital')
        res = super(HospitalPatient, self).create(vals)
        #print("Res-->", res)
        #print("Vals-->", vals)
        return res
#to override get default values in fields
    #@api.model
    #def default_get(self, fields):
        #res = super(HospitalPatient, self).default_get(fields)
        #return res