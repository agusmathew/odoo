openerp.offers_app = function(instance, local) {
	local.product_button= instance.Widget.extend({
        template: "product_template",
        events:{
            'click #apply_id':'product_apply',
            	}
        product_apply: function(event) {
        	var product_apply_fun = new instance.web.Model('button.demo');
                product_apply_fun.call('apply_button')
                });