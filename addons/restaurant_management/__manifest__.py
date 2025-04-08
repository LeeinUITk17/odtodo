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
    'depends': ['base','web','mail'],  # Ensure dependencies are correct
    'data': [
        'security/restaurant_management_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/branch_views.xml',
        'views/table_views.xml',
        'views/category_views.xml',
        # Đưa file wizard lên TRƯỚC các file view sử dụng nó
        'wizard/add_menu_item_wizard_views.xml', # <<< LOAD WIZARD VIEW TRƯỚC
        'views/order_views.xml',                  # <<< LOAD ORDER VIEW SAU
        'views/menu_item_views.xml',          # (menu_item_view cũng nên load sau wizard nếu có dùng)
        'views/reservation_views.xml',
        'views/invoice_views.xml',
        'views/customer_views.xml',
    ],
     # THÊM PHẦN ASSETS
    'assets': {
        'web.assets_backend': [
            'restaurant_management/static/src/css/order_form_kanban.css',
            'restaurant_management/static/src/css/form_button_box.css',
            'restaurant_management/static/src/css/invoice_form.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
