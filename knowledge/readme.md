Knowledge module migration
--------------------------

This module is an official module but was not present in odoo 9.0 official repository
so we took it from Odoo 8.0 repository and add it here.

Here are the modification that have been done to make it work

We added views folder
we moved Knowledge_view.xml and res_config_view.xml to views
we renamed Knowledge_view.xml to Knowledge.xml and res_config_view.xml to res_config.xml

res_config view is edited so that knowledge setting is accessible the following way 
"knowledge/configuration/settings"

We added demo folder
we moved Knowledge_demo.xml to demo
we renamed Knowledge_demo.xml to Knowledge.xml and


we created models folder
we moved res_config.py to that folder and edited it to respect the new Odoo model api
#osv.osv_memory replace by models.TransientModel
#_columns replaced by _fields
we created the __init__.py file

we edited the __openerp__.py file to reflect the new folder structure
