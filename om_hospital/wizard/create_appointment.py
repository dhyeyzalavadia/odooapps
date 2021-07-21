
from odoo import api, fields, models, _

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    image = fields.Binary(string='Patient Image')
    date = fields.Date(string='Date', required=False, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=False)
#to save wizard data into database
    def action_create_appointment(self):
        vals={
            'patient_id':self.patient_id.id,
            'date':self.date
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
#to open new tab after making record in wizard
        return {
            'name': _('Appointment'),
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            #'target': 'new'
        }
    def action_view_appointment(self):
        action = self.env.ref('om_hospital.patient_appointment_action').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action
