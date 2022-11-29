{
    'name': 'Manufacturer',
    'version': '4.0',
    'sequence': '3',
    'author': 'Vishvash Vishwakarma',
    'website': 'https://www.zehntech.com/',
    'images': ['static/description/icon.png'],
    'category': 'Manufacturing',
    'depends': ['product'],
    'data': ['security/ir.model.access.csv',
             'data/cron_job.xml',
             'views/manufacturer_view.xml',
             'views/product_template_view.xml',
             'report/manufacturer_detail_report.xml'
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
