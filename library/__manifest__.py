{
    'name': 'zizou library_management_system',
    'version': '1.0',
    'website': 'zizoubouchelkia@gmail.com',
    'author': 'zizou bouchelkia',
    'description': """
        manage your library with our application
    """,
    'category': 'Sales',
    'depends': ["base","web","mail"],
    'data': [

        'security/ir.model.access.csv',
        'security/library_security.xml',

        'views/library_book.xml',
        'views/library_author.xml',
        'views/library_borrow.xml',
        'views/library_member.xml',
        'views/library_menus.xml',
        'views/library_book_topic.xml',
        'views/library_publisher.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [
            'library/static/src/css/library_borrow.css',
        ],
    },

    'images': ['static/description/livre.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
