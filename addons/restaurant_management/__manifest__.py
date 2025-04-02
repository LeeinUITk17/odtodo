{
    'name': 'Restaurant Management',
    'version': '1.0',
    'summary': 'Manage restaurant branches, tables, reservations, and customers',
    'description': """
        A module to manage restaurant operations including:
        - Branch management
        - Table reservations
        - Customer database
    """,
    'author': 'NexaLap',
    'website': 'https://www.odooclass.com', 
    'category': 'Restaurant',
    'depends': ['base','invoice_management','web'],  # Ensure dependencies are correct
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
