{
    'name': 'Restaurant Management',
    'version': '1.0',
    'summary': 'Manage restaurant branches, tables, reservations, and customers',
    'category': 'Restaurant', 
    'description': """
        A module to manage restaurant operations including:
        - Branch management
        - Table reservations
        - Customer database
    """,
    'author': 'NexaLap',
    'website': 'https://www.odooclass.com', 
    'category': 'Restaurant',
    'depends': ['base','web'],  # Ensure dependencies are correct
    'data': [
        'security/ir.model.access.csv',
        'views/branch_views.xml',
        'views/table_views.xml',  
        'views/category_views.xml',
        'views/menu_item_views.xml',
        'views/reservation_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
