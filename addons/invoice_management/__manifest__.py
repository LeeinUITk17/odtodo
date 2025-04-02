{
    'name': 'Invoice Management',
    'version': '1.0',
    'summary': 'Manage restaurant invoices efficiently',
    'description': """
        This module provides functionalities to manage invoices, 
        including invoice creation, payment tracking, and integration with orders.
    """,
    'category': 'Restaurant',
    'website': 'https://www.odooclass.com', 
    'author': 'NexaLap',
    'depends': ['base','restaurant_management','web'],  # Ensure dependencies are correct
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
