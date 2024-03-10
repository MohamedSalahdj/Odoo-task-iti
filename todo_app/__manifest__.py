{
    'name': "Todo App",
    'summary': """ to do app make you to manange your task""",
    'description': """ """,
    'author': "Mohamed Samy",
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': ['base'
                ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/ticket.xml',
    ],
}