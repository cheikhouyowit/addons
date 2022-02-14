# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, models
from datetime import datetime
from odoo.tools.misc import formatLang

class SaleInvoiceSummaryReport(models.AbstractModel):
    _name = 'report.dev_sale_invoice_summary.sale_invoice_summary_template'
    _description = 'Sale Invoice Summary PDF Report'

    def get_sale_invoice_data(self, record):
        so_inv_list = []
        gt = []
        if record.status == 'posted':
            sql_query = """SELECT id FROM account_move WHERE state = %s AND
            invoice_date >= %s AND invoice_date <= %s AND partner_id = %s AND
            type = 'out_invoice'"""
            params = (record.status, record.from_date,
                  record.to_date, record.partner_id.id)
        else:
            sql_query = """SELECT id FROM account_move WHERE invoice_payment_state = %s AND
            invoice_date >= %s AND invoice_date <= %s AND partner_id = %s AND
            type = 'out_invoice'"""
            params = ('paid', record.from_date,
                  record.to_date, record.partner_id.id)
        self.env.cr.execute(sql_query, params)
        results = self.env.cr.dictfetchall()
        print ("result========",results)
        if results:
            total = ''
            for inv in results:
                invoice_id = self.env['account.move'].browse(int(inv['id']))
                so_date = ''
                inv_date = ''
                print ("nov=========",invoice_id.invoice_origin)
                if invoice_id.invoice_origin:
                    so_id = self.env['sale.order'].search(
                        [('name', '=', invoice_id.invoice_origin)], limit=1)
                    if so_id:
                        date_only = datetime.strptime(
                            str(so_id.date_order), '%Y-%m-%d %H:%M:%S').date()
                        so_date = datetime.strptime(str(date_only),
                                                    "%Y-%m-%d").strftime(
                            '%d-%m-%Y')
                        inv_date = datetime.strptime(
                            str(invoice_id.invoice_date), "%Y-%m-%d").strftime(
                            '%d-%m-%Y')
                        gt.append(invoice_id.amount_total)
                        so_inv_list.append(
                            {'inv_number': invoice_id and
                                           invoice_id.name or '',
                             'so_number': invoice_id and invoice_id.invoice_origin
                                          or '',
                             'inv_date': inv_date,
                             'so_date': so_date,
                             'inv_total': invoice_id.amount_total})
            total = (sum(gt))
        else:
            total = ''
            so_inv_list = []
        return so_inv_list, total

    def formatted_amount(self, record, amount):
        if record.currency_id:
            final_amount = formatLang(self.env, amount,
                                currency_obj=record.currency_id)
            return final_amount
        else:
            return amount

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.invoice.summary'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.invoice.summary',
            'docs': docs,
            'get_sale_invoice_data': self.get_sale_invoice_data,
            'formatted_amount': self.formatted_amount
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
