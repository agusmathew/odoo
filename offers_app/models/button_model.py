from openerp import models, fields, api
 
class button_action_demo(models.Model):
    _name = 'button.demo'
    @api.model 
    def apply_button(self): 
        print 'fooooooooooooooo'*100