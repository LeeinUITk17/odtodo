{
    'name': 'Restaurant CRM & Loyalty',
    'version': '1.0',
    'summary': 'Manage customer loyalty, memberships, points, and promotions for restaurants',
    'description': """
        A module to enhance customer relationships and loyalty for restaurants:
        - Membership Tier Management
        - Customer Membership & Points Tracking
        - Point Transactions (Earn, Redeem, Bonus, etc.)
        - Marketing Campaigns
        - Promotion Pools & Codes Management
        - Customer Segmentation for Campaigns (future)
        - Customer Activity Logging (related to CRM actions)
    """,
    'author': 'NexaLap', 
    'website': 'https://www.odooclass.com', 
    'category': 'Restaurant/CRM',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_customer_views.xml', 
        'views/crm_logs_views.xml',    
        'views/membership_tier_views.xml', 
        'views/membership_views.xml', 
        'views/point_transaction_views.xml',  
        'wizard/assign_campaign_wizard_views.xml',
        'wizard/generate_promo_codes_wizard_views.xml', 
        'views/promotion_pool_views.xml',    
        'views/promotion_code_views.xml',
        'views/marketing_campaign_views.xml',
        'views/campaign_delivery_views.xml',      
        'views/crm_menus.xml',          
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
