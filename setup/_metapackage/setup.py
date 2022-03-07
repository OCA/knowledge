import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-attachment_category',
        'odoo13-addon-document_page',
        'odoo13-addon-document_page_approval',
        'odoo13-addon-document_page_group',
        'odoo13-addon-document_page_portal',
        'odoo13-addon-document_page_project',
        'odoo13-addon-document_page_reference',
        'odoo13-addon-document_page_tag',
        'odoo13-addon-document_url',
        'odoo13-addon-knowledge',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
