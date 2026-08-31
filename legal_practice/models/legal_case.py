from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LegalCase(models.Model):
    _name = 'legal.case'
    _description = 'Expediente Legal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'opening_date desc, id desc'

    display_name = fields.Char(
        string='Identificador de Expediente',
        compute='_compute_display_name',
        store=True,
    )

    case_type_id = fields.Many2one(
        'legal.case.type', string='Tipo de Proceso',
        required=True, tracking=True,
    )
    case_number = fields.Char(
        string='Número de Expediente', required=True, tracking=True,
    )
    case_year = fields.Char(
        string='Año', required=True, tracking=True,
        default=lambda self: str(fields.Date.context_today(self).year),
    )
    court_id = fields.Many2one(
        'legal.court', string='Juzgado', required=True, tracking=True,
    )

    client_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True
        )
    opposing_party = fields.Char(string='Contraparte')
    lawyer_id = fields.Many2one(
        'res.users', string='Abogado Responsable',
        default=lambda self: self.env.user, tracking=True,
    )

    state = fields.Selection([
        ('nuevo', 'Nuevo'),
        ('en_proceso', 'En Proceso'),
        ('en_espera', 'En Espera'),
        ('cerrado', 'Cerrado'),
        ('archivado', 'Archivado'),
    ], string='Estado', default='nuevo', required=True, tracking=True)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Alta'),
        ('2', 'Urgente'),
    ], string='Prioridad', default='0')

    parent_case_id = fields.Many2one(
        'legal.case', string='Expediente de Origen',
        help='Úsalo cuando este expediente nace de otro, por ejemplo una '
             'apelación o un amparo derivado de un juicio anterior.',
    )
    related_case_ids = fields.One2many(
        'legal.case', 'parent_case_id', string='Expedientes Relacionados',
    )

    judge_id = fields.Many2one(
        'legal.judge', string='Juez / Magistrado',
        domain="[('court_id', '=', court_id)]",
    )

    sentencia_ids = fields.One2many(
        'legal.case.sentencia', 'case_id', string='Sentencias',
    )
    sentencia_count = fields.Integer(compute='_compute_sentencia_count')

    def _compute_sentencia_count(self):
        for rec in self:
            rec.sentencia_count = len(rec.sentencia_ids)

    opening_date = fields.Date(
        string='Fecha de Apertura',
        default=fields.Date.context_today,
        required=True,
    )
    closing_date = fields.Date(string='Fecha de Cierre')
    description = fields.Text(string='Descripción / Objeto del Caso')

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
        )

    _case_identity_uniq = models.Constraint(
        'UNIQUE(case_type_id, case_number, case_year, court_id)',
        'Ya existe un expediente con ese tipo, número y año en el mismo juzgado.',
    )

    @api.depends('case_type_id', 'case_number', 'case_year', 'court_id')
    def _compute_display_name(self):
        for rec in self:
            if (rec.case_type_id and rec.case_number and rec.case_year and
                    rec.court_id):
                rec.display_name = (
                    f"{rec.case_type_id.name} {rec.case_number}/{rec.case_year} "
                    f"- {rec.court_id.name}"
                )
            else:
                rec.display_name = 'Nuevo Expediente'

    @api.constrains('opening_date', 'closing_date')
    def _check_dates(self):
        for rec in self:
            if rec.closing_date and rec.opening_date and rec.closing_date < rec.opening_date:
                raise ValidationError(
                    'La fecha de cierre no puede ser anterior a la fecha de apertura.'
                )

    def action_set_en_proceso(self):
        self.write({'state': 'en_proceso'})

    def action_set_en_espera(self):
        self.write({'state': 'en_espera'})

    def action_close_case(self):
        for rec in self:
            if not rec.closing_date:
                rec.closing_date = fields.Date.context_today(rec)
        self.write({'state': 'cerrado'})

    def action_archive_case(self):
        self.write({'state': 'archivado', 'active': False})
