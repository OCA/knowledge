import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-document_page>=15.0dev,<15.1dev',
        'odoo-addon-document_page_approval>=15.0dev,<15.1dev',
        'odoo-addon-document_page_group>=15.0dev,<15.1dev',
        'odoo-addon-document_page_reference>=15.0dev,<15.1dev',
        'odoo-addon-document_page_tag>=15.0dev,<15.1dev',
        'odoo-addon-document_url>=15.0dev,<15.1dev',
        'odoo-addon-knowledge>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
