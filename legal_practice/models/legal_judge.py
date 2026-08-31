from odoo import models, fields


class LegalJudge(models.Model):
    _name = 'legal.judge'
    _description = 'Juez / Magistrado'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    position = fields.Selection([
        ('juez', 'Juez'),
        ('magistrado', 'Magistrado'),
        ('magistrado_presidente', 'Magistrado Presidente'),
    ], string='Cargo', required=True, default='juez')
    court_id = fields.Many2one(
        'legal.court', string='Juzgado / Tribunal Actual', required=True,
    )
    active = fields.Boolean(default=True)

    sentencia_ids = fields.One2many(
        'legal.case.sentencia', 'judge_id', string='Sentencias Emitidas',
    )
    sentencia_count = fields.Integer(compute='_compute_sentencia_count')

    def _compute_sentencia_count(self):
        for rec in self:
            rec.sentencia_count = len(rec.sentencia_ids)
