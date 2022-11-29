from odoo import models, fields, api, _
import requests
import random
from odoo.exceptions import MissingError
from odoo.exceptions import ValidationError
import logging

# Manufacturer Model Code
_logger = logging.getLogger(__name__)


class ManufacturerDetails(models.Model):
    _name = 'manufacturer.detail'
    _description = 'User able to store manufacturer data'
    _rec_name='cname'

    # Basic Fields
    cname = fields.Char(string='Company Name', required=True)
    owner = fields.Char(string='Owner Name')

    country = fields.Many2one('res.country', string='Country')
    state = fields.Char(string='State')
    city = fields.Char(string='City')
    street = fields.Char(string='Street Address')
    pincode = fields.Char(string='Zip Code / Pin Code')

    email = fields.Char(string='Email', required=True)
    aemail = fields.Char(string='Alternate Email')
    website = fields.Char(string='Website', required=True)
    fax = fields.Char(string='Fax')

    phone = fields.Char(string='Mobile No.')
    aphone = fields.Char(string='Alternate Mobile No.')
    lphone = fields.Char(string='Landline/TelePhone.')

    # Applying Validation
    # Checking mobile number is valid or not
    @api.onchange('phone')
    def check_phone(self):
        if self.phone:
            res = ((str(self.phone)).isdigit() == True) and (
                len(str(self.phone)) == 10)
            if not res:
                raise ValidationError(
                    " Please enter a valid 10 digit mobile number")

    # Checking aternate mobile number is valid or not
    @api.onchange('aphone')
    def check_aphone(self):
        if self.aphone:
            res = ((str(self.aphone)).isdigit() == True) and (
                len(str(self.aphone)) == 10)
            if not res:
                raise ValidationError(
                    " Please enter a valid 10 digit alternate mobile number")

    # Manufacturer data pulled from api
    # Cron Job / Scheduled Action code for fetching data from API
    @api.model
    def pull_data_from_api(self):
        try:
            # API information
            url = "https://twelve-data1.p.rapidapi.com/stocks"

            querystring = {"exchange": "NASDAQ", "format": "json"}

            headers = {
                'x-rapidapi-host': "twelve-data1.p.rapidapi.com",
                'x-rapidapi-key': self.env['ir.config_parameter'].get_param('x-rapidapi-key', False)
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            data = response.json()

            # collecting data from api
            company_data = data['data']

            # Storing required data from complete data
            for comp_data in company_data:
                company_name = comp_data['name']
                company_country = comp_data['country']

                # logics for removing spaces . , ' from company name for website url and email address
                mail_web_data = company_name
                mail_web_data = mail_web_data.replace(" ", "")
                mail_web_data = mail_web_data.replace("'", "")
                mail_web_data = mail_web_data.replace(".", "")
                mail_web_data = mail_web_data.replace(",", "")
                mail_web_data = mail_web_data.lower()
                rand = str(random.randint(0, 999))

                # Generating Mobile Number
                m_num = str(random.randint(1000000000, 9999999999))

                # creating "email address" and "website url" from company name
                company_email = mail_web_data + rand + "@gmail.com"
                company_website = "https://www." + mail_web_data + ".com"

                # Searching country id for Many2one field
                country_id = self.env['res.country'].search(
                    [('name', '=', company_country)])

                # Create ORM for create data in manufacturer module
                self.env['manufacturer.detail'].create({
                    'cname': company_name,
                    'country': country_id[0].id,
                    'email': company_email,
                    'website': company_website,
                    'phone': m_num
                })

            # logger for cron job execution information
            _logger.info(
                '"Manufacturer data fetched successfully from API." Cron job executed successfully.')

        except:
            # logger for showing error on terminal
            _logger.error(
                "Unable to fetch manufacturer data from API. Something missing please checkout.")

            # Raising error on odoo user interface
            raise MissingError(
                ' "Unable to fetch manufacturer data from API."\
                    Please checkout API key is available or not for you.\
                        Otherwise check your internet connection for fetching data from API.')
