from odoo import http
from odoo.http import request


class YourController(http.Controller):
    @http.route('/url', type='http',auth='public',website=True)
    def get_between_records(self, **kw):
        records = request.env['sale.order'].search([])  # Customize the search domain as needed
        return request.render('scheduler.search_model_faculty_time_table', {'records': records})