# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
{
    'name': 'URL attachment',
    'version': '9.0.1.0.0',
    'category': 'Tools',
    'description': """
Module that allows to attach an URL as a document.
    """,
    'author': "Serv. Tecnolog. Avanzados - Pedro M. Baeza,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.serviciosbaeza.com',
    'license': 'AGPL-3',
    'depends': [
        'document',
    ],
    'data': [
        'view/document_url_view.xml',
    ],
    'qweb': [
        'static/src/xml/url.xml',
    ],
    'installable': True,
}
