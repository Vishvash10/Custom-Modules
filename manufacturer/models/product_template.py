from odoo import models, fields, _

# product template
class ProductTemplateInherit(models.Model):
    _inherit = "product.template"
    manufact_details_ids = fields.One2many(
        'product.template.line', 'company_detail_id', string='Manufacturer Details')


class ProductTemplateLine(models.Model):
    _name = 'product.template.line'
    _description = 'Adding new tab field in product template'

    #For resloving errors related to product template fields
    company_detail_id = fields.Many2one(
        'product.template', string='Company Details', ondelete='cascade')

    #Required fields for displaying manufacturer data in product template.
    company_name = fields.Many2one(
        'manufacturer.detail', string='Company Name')
    company_email = fields.Char(related='company_name.email',string='Company Email')
    company_website = fields.Char(related='company_name.website',string='Company Website')

    