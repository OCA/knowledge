import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-attachment_category',
        'odoo14-addon-attachment_preview',
        'odoo14-addon-attachment_zipped_download',
        'odoo14-addon-document_page',
        'odoo14-addon-document_page_access_group',
        'odoo14-addon-document_page_approval',
        'odoo14-addon-document_page_group',
        'odoo14-addon-document_page_project',
        'odoo14-addon-document_page_reference',
        'odoo14-addon-document_page_tag',
        'odoo14-addon-document_url',
        'odoo14-addon-knowledge',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
