from odoo import models, fields,api
from odoo import http
# product model
class Product(models.Model):

    _name = "product"
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Product Code', required=True)
    price = fields.Integer(string='Price', required=True)
    stock = fields.Integer(string='Stock')
    date = fields.Date(string="Date")
    offer_code =  fields.Char(string='Offer Code')
# funtion to check offer and apply available offer code when the buy button is clicked
    def buy_add (self):
        
        products = self.env['product'].search([('code','=',self.code)])
        offers = self.env['offer'].search([])

        product_code = products.code if products else None
        product_stock = products.stock if products else None
        product_offer = products.offer_code if products else None
        product_price = products.price if products else None
        price = None     

        # if the product is available     
        if product_stock and product_code:
            for offer in offers:
                offer_code = offer.code if offer else None
                print [i.code for i in offer.products],"10"*100
                if product_offer:
                    if product_offer == offer_code and product_code in [i.code for i in offer.products]:
                        offer_start_date = offer.start
                        offer_end_date = offer.end
                        offer_discount_type = offer.discount
                        offer_amount = offer.amount
                        if offer_discount_type == 'p':
                            product_offer_price = product_price-product_price*offer_amount/100
                            price = product_offer_price
                        elif offer_discount_type == 'r':
                            product_offer_price = product_price - offer_amount
                            price = product_offer_price
                    else:
                        price = product_price
        if price:
            dict1 = {
            'name': products.name,
            'code': product_code,
            'price': price,
            'date':products.date,
            'stock':product_stock,

            }
            inv_obj = self.env['pop']
            invoice = inv_obj.create(dict1)
            dict1['resid'] = invoice.id
            print '11'*100, invoice.id,"22"*100
            return self.buy_method(dict1)

    @api.multi
    def buy_method(self,dict1):
        
        view_id = self.env.ref('offers_app.view_pop_form').id
        context = self._context.copy()
        return {
            'name':'Offer Applied Succesfully',
            'view_type':'form',
            'view_mode':'form',
            'views' : [(view_id,'form')],
            'res_model':'pop',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':dict1['resid'],
            'target':'new',
            'context':context,
        }

# Transient Model to save product details after the offer code is applied
class Pop(models.TransientModel):
    _name = "pop"
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Product Code', required=True)
    price = fields.Integer(string='Offer Price', required=True)
    date = fields.Date(string="Date")
    stock = fields.Integer(string='Stock')


            
            

        

        # for product in products:
        #     if product

# offers model which contains all the offers and their details    
class Offer(models.Model):

    _name = "offer"
    code = fields.Char(string='Offer Code', required=True)
    stock = fields.Integer(string='Stock')
    start = fields.Date(string="Start Date")
    end = fields.Date(string="End Date")
    discount = fields.Selection([('p', 'Percentage'), ('r', 'rupee'),], string='Discount Type')
    amount = fields.Integer(string='Discount')
    products = fields.Many2many('product',string='Product Code')


