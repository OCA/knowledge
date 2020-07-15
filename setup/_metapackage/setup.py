import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-attachment_preview',
        'odoo12-addon-document_page',
        'odoo12-addon-document_page_approval',
        'odoo12-addon-document_page_group',
        'odoo12-addon-document_page_project',
        'odoo12-addon-document_page_reference',
        'odoo12-addon-document_page_tag',
        'odoo12-addon-document_url',
        'odoo12-addon-knowledge',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
