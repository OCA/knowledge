import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-attachment_zipped_download>=16.0dev,<16.1dev',
        'odoo-addon-document_knowledge>=16.0dev,<16.1dev',
        'odoo-addon-document_page>=16.0dev,<16.1dev',
        'odoo-addon-document_page_access_group>=16.0dev,<16.1dev',
        'odoo-addon-document_page_access_group_user_role>=16.0dev,<16.1dev',
        'odoo-addon-document_page_approval>=16.0dev,<16.1dev',
        'odoo-addon-document_page_group>=16.0dev,<16.1dev',
        'odoo-addon-document_page_partner>=16.0dev,<16.1dev',
        'odoo-addon-document_page_project>=16.0dev,<16.1dev',
        'odoo-addon-document_page_reference>=16.0dev,<16.1dev',
        'odoo-addon-document_page_tag>=16.0dev,<16.1dev',
        'odoo-addon-document_url>=16.0dev,<16.1dev',
        'odoo-addon-document_url_google_drive>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
