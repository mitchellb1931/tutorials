{
    'name': 'Gestión de Despacho Legal',
    'version': '19.0.1.0.0',
    'category': 'Services/Legal',
    'summary': 'Gestión de expedientes, clientes y casos para despachos de abogados',
    'description': """
        Módulo para la gestión integral de un despacho legal:
        - Expedientes / casos
        - Clientes
        - (Próximamente) Agenda de citas y gestión documental
    """,
    'author': 'Tu Despacho',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/legal_practice_security.xml',
        'security/ir.model.access.csv',
        'views/legal_case_type_views.xml',
        'views/legal_court_views.xml',
        'views/legal_judge_views.xml',
        'views/legal_case_views.xml',
        'views/legal_practice_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
