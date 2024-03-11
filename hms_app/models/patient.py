from odoo import models, fields, api, exceptions

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html(string='History', invisible=True)
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor')
    department_capacity = fields.Integer(related='department_id.capacity')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ])
    email = fields.Char(string='Email', required=True, unique=True)
    history_ids = fields.One2many('patient.history', 'patient_id', string='History')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id and not self.department_id.is_opened:
            self.department_id = False
            return {'warning': {'title': 'Closed Department', 'message': 'You cannot select a closed department.'}}

    def write(self, vals):
        if 'state' in vals:
            description = f'State changed to {vals["state"].capitalize()}'
            self.history_ids.create({'created_by': self.env.user.id, 'description': description})
        return super(Patient, self).write(vals)

    @api.constrains('pcr')
    def _check_cr_ratio(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise exceptions.ValidationError("CR Ratio field is mandatory when PCR is checked.")

    @api.depends('age')
    def _compute_history_visibility(self):
        for patient in self:
            if patient.age and patient.age < 50:
                patient.history = False
            else:
                patient.history = True

    @api.onchange('age')
    def _onchange_age(self):
        for patient in self:
            if patient.age and patient.age < 30:
                patient.pcr = True
                return {
                    'warning': {
                        'title': 'Note',
                        'message': 'PCR has been checked',
                        'type': 'notification',
                    },
                }
            else:
                patient.pcr = False

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                patient.age = today.year - patient.birth_date.year - (
                        (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
            else:
                patient.age = False
