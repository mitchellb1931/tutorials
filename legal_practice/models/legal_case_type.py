from odoo import models, fields


class LegalCaseType(models.Model):
    _name = 'legal.case.type'
    _description = 'Tipo de Proceso Legal'
    _order = 'name'

    name = fields.Char(string='Tipo de Proceso', required=True)
    active = fields.Boolean(default=True)

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'Ya existe un tipo de proceso con ese nombre.',
    )
