# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Atachment Category',
    'summary': """
        Adds a document category to help classification""",
    'version': '12.0.1.0.1',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'depends': [
        "base",
    ],
    'data': [
        'views/ir_attachment.xml',
        'security/ir_attachment_category.xml',
        'views/ir_attachment_category.xml',
    ],
}
