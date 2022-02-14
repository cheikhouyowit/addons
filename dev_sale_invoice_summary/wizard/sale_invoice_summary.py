# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, fields, models, _
import xlwt
from xlwt import easyxf
from datetime import datetime
from io import BytesIO
import base64
from odoo.tools.misc import formatLang


class SaleInvoiceSummary(models.TransientModel):
    _name = "sale.invoice.summary"

    from_date = fields.Date("From Date", required=True)
    to_date = fields.Date("To Date", required=True)
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 required=True)
    status = fields.Selection([('posted', 'Posted'), ('paid', 'Paid')],
                              default='posted', required=True)

    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        default=lambda self: self.env.user.company_id.currency_id)

    def print_pdf(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref(
            'dev_sale_invoice_summary.print_sale_invoice_summary').report_action(
            self, data=None)

    def formatted_amount(self, amount):
        if self.currency_id:
            final_amount = formatLang(self.env, amount,
                                currency_obj=self.currency_id)
            return final_amount
        else:
            return amount

    def print_excel(self):
        filename = 'Sale/Invoice Summary.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sale / Invoice')

        # defining various font styles
        style1 = easyxf('font:height 200;align: horiz center;font:bold True;')
        text_center = easyxf('align: horiz center;')
        text_right = easyxf('align: horiz right;')

        # setting with of the column
        worksheet.col(0).width = 70 * 70
        worksheet.col(1).width = 70 * 70
        worksheet.col(2).width = 70 * 70
        worksheet.col(3).width = 70 * 70
        worksheet.col(4).width = 80 * 80

        # in merge 1,2 is height[index of cell] ans 1,5 is width[index if cell]
        worksheet.write_merge(1, 2, 0, 2, 'Sale/Invoice Summary', easyxf(
            'font:height 380;align: horiz center;font: color blue; font:bold True;'))

        # writting into the sheet (Labels)
        worksheet.write(1, 3, "From Date", style1)
        worksheet.write(2, 3, "To Date", style1)
        worksheet.write(1, 4, str(
            datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime(
                '%d-%m-%Y')))
        worksheet.write(2, 4, str(
            datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%d-%m-%Y')))
        worksheet.write(3, 1, "Customer", style1)
        worksheet.write_merge(3, 3, 2, 3, str(self.partner_id.name))
        state = ''
        if self.status == 'posted':
            state = 'Posted'
        else:
            state = 'Paid'
        worksheet.write(4, 1, "Invoice Status", style1)
        worksheet.write(4, 2, state)
        worksheet.write(6, 0, "Invoice Number", style1)
        worksheet.write(6, 1, "Sale Order Number", style1)
        worksheet.write(6, 2, "Invoice Date", style1)
        worksheet.write(6, 3, "Sale Order Date", style1)
        worksheet.write(6, 4, "Invoice Total", style1)

        if self.status == 'posted':
            sql_query = """SELECT id FROM account_move WHERE state = %s AND
            invoice_date >= %s AND invoice_date <= %s AND partner_id = %s AND
            type = 'out_invoice'"""
            params = ('posted', self.from_date, self.to_date, self.partner_id.id)
            self.env.cr.execute(sql_query, params)
        else:
            sql_query = """SELECT id FROM account_move WHERE invoice_payment_state = %s AND
            invoice_date >= %s AND invoice_date <= %s AND partner_id = %s AND
            type = 'out_invoice'"""
            params = ('paid', self.from_date, self.to_date, self.partner_id.id)
            self.env.cr.execute(sql_query, params)
            
        results = self.env.cr.dictfetchall()
        if results:
            start = 7
            gt = []
            for inv in results:
                invoice_id = self.env['account.move'].browse(int(inv['id']))
                so_no = ''
                so_date = ''
                if invoice_id.invoice_origin:
                    so_no = invoice_id.invoice_origin
                    so_id = self.env['sale.order'].search(
                        [('name', '=', invoice_id.invoice_origin)], limit=1)
                    if so_id:
                        date_only = \
                            datetime.strptime(str(so_id.date_order),
                                              '%Y-%m-%d %H:%M:%S').date()
                        so_date =\
                            datetime.strptime(str(date_only),
                                              "%Y-%m-%d").strftime('%d-%m-%Y')
                        worksheet.write(start, 0, invoice_id.name, text_center)
                        worksheet.write(start, 1, so_no, text_center)
                        worksheet.write(start, 2, datetime.strptime(
                            str(invoice_id.invoice_date), "%Y-%m-%d") \
                                        .strftime('%d-%m-%Y'), text_center)
                        worksheet.write(start, 3, so_date, text_center)
                        inv_total = \
                            self.formatted_amount(invoice_id.amount_total)
                        gt.append(invoice_id.amount_total)
                        worksheet.write(start, 4, inv_total, text_center)
                        start += 1
            final_total = self.formatted_amount(sum(gt))
            worksheet.write(start + 1, 3, 'Grand Total', style1)
            worksheet.write(start + 1, 4, final_total, text_center)

        # exporting excel process
        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['sale.invoice.summary.excel'].create(
            {'excel_file': base64.encodestring(fp.getvalue()),
             'file_name': filename})
        fp.close()
        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'sale.invoice.summary.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new'
        }


class SaleInvoiceSummaryExcel(models.TransientModel):
    _name = "sale.invoice.summary.excel"
    _description = "Sale Invoice Summary Excel Report"
    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File', size=64)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
