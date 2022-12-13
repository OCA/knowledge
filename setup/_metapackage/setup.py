import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-knowledge",
    description="Meta package for oca-knowledge Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-document_knowledge>=16.0dev,<16.1dev',
        'odoo-addon-document_page>=16.0dev,<16.1dev',
        'odoo-addon-document_page_group>=16.0dev,<16.1dev',
        'odoo-addon-document_page_tag>=16.0dev,<16.1dev',
        'odoo-addon-document_url>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
