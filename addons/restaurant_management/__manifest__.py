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
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/restaurant_management_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/res_users_views.xml',
        'views/branch_views.xml',
        'views/table_views.xml',
        'views/category_views.xml',
        'wizard/add_menu_item_wizard_views.xml',
        'views/order_views.xml',
        'views/menu_item_views.xml',
        'views/reservation_views.xml',
        'views/invoice_views.xml',
        'views/customer_views.xml',
        # 'views/waiter_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'restaurant_management/static/src/css/order_form_kanban.css',
            'restaurant_management/static/src/css/form_button_box.css',
            'restaurant_management/static/src/css/invoice_form.css',
            'restaurant_management/static/src/css/waiter_order_screen.css',
            'restaurant_management/static/src/js/components/table_list.js',
            'restaurant_management/static/src/js/components/menu_grid.js',
            'restaurant_management/static/src/js/components/order_cart.js',
            # 'restaurant_management/static/src/js/waiter_order_screen.js',
            # 'restaurant_management/static/src/js/waiter_app.js',
        ],
        # 'web.assets_qweb': [
        #     'restaurant_management/static/src/xml/components/table_list.xml',
        #     'restaurant_management/static/src/xml/components/menu_grid.xml',
        #     'restaurant_management/static/src/xml/components/order_cart.xml',
        #     'restaurant_management/static/src/xml/waiter_order_screen.xml',
        # ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
