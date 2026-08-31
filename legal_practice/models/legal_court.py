from odoo import models, fields


class LegalCourt(models.Model):
    _name = 'legal.court'
    _description = 'Juzgado / Tribunal'
    _order = 'name'

    name = fields.Char(string='Juzgado', required=True)
    court_type = fields.Selection([
        ('juzgado_distrito', 'Juzgado de Distrito'),
        ('tribunal_colegiado', 'Tribunal Colegiado de Circuito'),
        ('tribunal_unitario', 'Tribunal Unitario de Circuito'),
        ('tribunal_superior', 'Tribunal Superior de Justicia'),
        ('juzgado_local', 'Juzgado Local / Estatal'),
        ('otro', 'Otro'),
    ], string='Tipo de Órgano Jurisdiccional')
    district = fields.Char(string='Distrito / Circuito')
    city = fields.Char(string='Ciudad')
    active = fields.Boolean(default=True)

    judge_ids = fields.One2many(
        'legal.judge', 'court_id', string='Jueces / Magistrados Adscritos',
    )
    # mesa_ids: pendiente, se agrega después sin afectar lo existente