# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Sale/Invoice Summary Report',
    'version': '13.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
 odoo App will Print Sale/Invoice Summary in PDF Report
        
        Sale Summary , Invoice Summary, Sale invoice Summary , Sale by dates, Invoice by Dates, Sale Invoice by Dates
Sale/Invoice Summary Report
Odoo Sale/Invoice Summary Report
Sale summary report 
Odoo sale summary report 
Invoice summary report 
Odoo invoice summary report 
Sale report 
Odoo sale report 
Invoice report 
Odoo invoice report
Print sale report 
Odoo print sale report 
Print invoice report 
Odoo print invoice report
Print sale summary report 
Odoo print sale summary report 
Print Sale/Invoice Summary Report into PDF format
Odoo Print Sale/Invoice Summary Report into PDF format
Print sale summary report into pdf format 
Odoo print sale summary report into pdf format 
Print invoice summary report into pdf format 
Odoo print invoice summary report into pdf format 
Print sale report into pdf format 
Odoo print sale report into pdf format 
Print invoice report into pdf format 
Odoo print invoice report into pdf format 
Odoo App Print Sale/Invoice Summary in PDF Report, sale invoice details, sale invoice summary, sale summary, sale invoice, sale invoice status, sale invoice report, Sale by dates, Invoice by Dates, Sale Invoice by Dates,Sale Summary , Invoice Summary, Sale invoice Summary

    """,
    'summary': 'Odoo App Print Sale/Invoice Summary in PDF Report, sale invoice details, sale invoice summary, sale summary, sale invoice, sale invoice status, sale invoice report, Sale by dates, Invoice by Dates, Sale Invoice by Dates,Sale Summary , Invoice Summary, Sale invoice Summary',
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/security.xml',
        'wizard/sale_invoice_summary_view.xml',
        'report/sale_invoice_summary_report_menu.xml',
        'report/sale_invoice_summary_report_template.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':19.0,
    'currency':'EUR',
   # 'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
