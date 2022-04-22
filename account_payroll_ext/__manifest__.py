{
    'name': 'account payroll ext',

    'version': '14.0.0.0',

    'author': "ProcessControl",

    'contributors': ['Luis Felipe Paternina'],

    'website': "www.processcontrol.es",

    'category': 'Account',

    'depends': [

        'account_accountant',
        'hr',
        'hr_attendance',
        'bim_project',
    ],

    'data': [
        
        'security/security.xml',
        'security/ir.model.access.csv',
        #'views/res_company.xml',
               
    ],
    'installable': True
}
