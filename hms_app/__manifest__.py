{
    'name': "HMS App",
    'summary': """ Hospital Management System """,
    'description': """ """,
    'author': "Mohamed Samy",
    'category': 'Services',
    'version': '17.0.0.1.0',
    'depends': ['base'
                ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/doctor.xml',
        'views/patient.xml',
        'views/department.xml'
    ],
}