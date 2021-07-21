from odoo import api, fields, models, _
class Doctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Doctor Details"

    image = fields.Binary(string='Doctor Image')
    referance = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                            default=lambda self: _('Om Hospital Doctor'))
    patient_id = fields.Many2one('hospital.appointment', string="Patient", required=True,)
    name = fields.Char(string='Name', required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'cancelled')], default="draft", string="States",
                             tracking=True, related='patient_id.state')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    time = fields.Datetime(string='Appointment Time', related='patient_id.time')
    note = fields.Text(string='Description', tracking=True)
    specialist = fields.Selection([
        ('dentist', 'Dentist'),
        ('cardiologist', 'Cardiologist'),
        ('ent_specialist', 'ENT Specialist'),
        ('gynaecologist', 'Gynaecologist'),
        ('orthopaedic_surgeon', 'Orthopaedic surgeon'),
        ('radiologist', 'Radiologist'),
        ('md_surgeon', 'Md surgeon'),
        ('neurologist', 'Neurologist'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    #appointment_count = fields.Integer(string='Total Appointments', compute='compute_appointment_count')



