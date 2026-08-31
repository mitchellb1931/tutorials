from odoo import models, fields


class LegalCaseSentencia(models.Model):
    _name = 'legal.case.sentencia'
    _description = 'Sentencia / Resolución'
    _order = 'date desc'

    case_id = fields.Many2one(
        'legal.case', string='Expediente', required=True, ondelete='cascade',
    )
    judge_id = fields.Many2one(
        'legal.judge', string='Juez / Magistrado que Resuelve',
    )
    sentencia_type = fields.Selection([
        ('interlocutoria', 'Interlocutoria'),
        ('definitiva', 'Definitiva'),
        ('otro', 'Otra Resolución'),
    ], string='Tipo de Resolución', required=True, default='definitiva')
    date = fields.Date(
        string='Fecha de la Resolución', required=True,
        default=fields.Date.context_today,
    )
    sentido = fields.Selection([
        ('favorable', 'Favorable'),
        ('desfavorable', 'Desfavorable'),
        ('parcial', 'Parcialmente Favorable'),
        ('otro', 'Otro / No Aplica'),
    ], string='Sentido')
    summary = fields.Text(string='Resumen')