{
    'name': 'Real Estat Ads zizou',
    'version': '1.0',
    'website': 'zizoubouchelkia@gmail.com',
    'author': 'zizou bouchelkia',
    'description': """
        Real Estate module to show available properties
    """,
    'category': 'Sales',
    'depends': ["base","mail"],
    'data': [
        #groups
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        'views/property_view.xml',
        'views/property_offer_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

        # Uncomment if you want to load this data file
        # 'data/property_type.xml'
        'data/estat.property.type.csv',

        #reports
        'report/property_report.xml',
        'report/report_template.xml',
    ],
    'demo': [
        'demo/property_tag.xml',
    ],
    'assets': {
      'web.assets_backend': [
            'real_estat_ads/static/src/js/my_custom_tag.js',
            'real_estat_ads/static/src/xml/my_custom_tag.xml',

        ]
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
