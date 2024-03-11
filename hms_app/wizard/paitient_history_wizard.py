from odoo import models, fields

class PatientHistory(models.Model):
    _name = 'patient.history'
    _description = 'Patient History Wizard'

    patient_id = fields.Many2one('hms.patient', string='Patient')
    created_by = fields.Char(default=lambda self: self.env.user.name)
    date = fields.Date(default=fields.Date.today)
    description = fields.Text(string='Description')
