from odoo import api, fields, models, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                            default=lambda self: _('Appointment'), related='patient_id.referance')
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'cancelled')], default="draft", string="States",
                             tracking=True, related='patient_id.state')
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
    date = fields.Date(string='Appointment Date')
    referred = fields.Many2one('hospital.doctor', string="Referred to", required=True, related='patient_id.referred')
    time = fields.Datetime(string='Checkup Time')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True, related='patient_id.gender')
    note = fields.Text(string='Description', related='patient_id.note', tracking=True)
    appointment_count = fields.Integer(string='Total Appointments', related='patient_id.appointment_count')

    #def compute_appointment_count(self):
        #for rec in self:
            #appointment_count=self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            #rec.appointment_count = appointment_count

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        #if not vals.get('note'):
            #vals['note'] = 'New Patient'
        if vals.get('sequence', _('Appointment')) == _('Appointment'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('Appointment')
        res = super(HospitalAppointment, self).create(vals)
        #print("Res-->", res)
        #print("Vals-->", vals)
        return res
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            #if self.patient_id.gender:
                #self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''
