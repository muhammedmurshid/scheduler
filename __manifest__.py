{
    'name': "Class Scheduler",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'faculty', 'logic_base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/scheduler_rules.xml',
        'views/class_schedular.xml',
        'views/re_scheduler_wizard.xml',
        'views/class_pdf_report.xml',
        'views/faculty_wizard.xml',
        'data/activity.xml',
        'views/search_wizard.xml',

    ],
    'demo': [],
    'summary': "logic_class_scheduler",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
