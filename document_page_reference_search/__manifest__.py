# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Document Page Reference Search',
    'summary': """
        Search on other modules from document page as references""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/knowledge',
    'depends': [
        'document_page_reference',
    ],
    'data': [
        'data/parameters.xml',
        'security/ir.model.access.csv',
        'views/document_page_reference_rule.xml',
    ],
}
