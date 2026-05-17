{
    'name': 'Service Contracts',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Manage service contracts and support requests',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/service_contract_views.xml',
        'views/service_request_views.xml',
        'views/menu.xml',
        'report/contract_report_action.xml',
        'report/contract_report.xml',
        'data/mail_template.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
