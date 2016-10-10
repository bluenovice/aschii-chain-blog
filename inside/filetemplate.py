import webapp2

form_html="""
	<form action="/">
	<input name="food" type="text">
	%s
	<input type="submit" name="add">
	</form>
"""
output_cart="""
<h2> <b>tis is the cart</h2>
<ul>
%s
</ul>
"""
hidden_html="""
	<input type="hidden" name="food" value="%s">
"""
items_html = "<li>%s</li>"
class MainHandler(webapp2.RequestHandler):
    def writes(self, *a, **kw):
        self.response.out.write(*a,**kw)

class Handler(MainHandler):
	def get(self):
		output = form_html
		outpuT_hidden = ""
		items = self.request.get_all("food")	
		if items:
			output_items=""
			for item in items:
				outpuT_hidden += hidden_html % item
				output_items += items_html % item

			output_shopping = output_cart% output_items
			output += output % output_shopping
			
		output = output % outpuT_hidden
		self.writes(output)
app = webapp2.WSGIApplication([
    ('/',Handler)
], debug=True)
