# the import section
import webapp2
import jinja2
import os
from models import Meme

# this initializes the jinja2 environment
# this will be the same in every app that uses the jinja2 templating library 
the_jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

# other functions should go above the handlers or in a separate file


# the handler section
class EnterInfoHandler(webapp2.RequestHandler):
  def get(self):  # for a get request
    welcome_template = the_jinja_env.get_template('templates/welcome.html')
    variable_dict = {
      "greeting":"Greetings",
      "adjective": "beautiful"
    }
    self.response.write(welcome_template.render(variable_dict))  # the response

class ResultsPage(webapp2.RequestHandler):
  def get(self):  # for a get request
    self.response.write("Please return to the home page to generate a meme!")  # the response

  def post(self):
    results_template = the_jinja_env.get_template('templates/results.html')
    meme_first_line = self.request.get('user-first-ln')
    meme_second_line = self.request.get('user-second-ln')
    meme_img_choice = self.request.get('meme-type')

    user_meme = Meme(first_line = meme_first_line, 
      second_line = meme_second_line,
      pic_type = meme_img_choice)
    user_meme.put()
    variable_dict = {"line1": meme_first_line, 
      "line2": meme_second_line, 
      "image_url": user_meme.get_meme_url()}
    self.response.write(results_template.render(variable_dict))

class MainPage(webapp2.RequestHandler):
  def get(self): 
	self.response.headers['Content-Type'] = 'text/html'
	self.response.write('<h1>Hello, CSSI!</h1>') 

class SecretPage(webapp2.RequestHandler):
  def get(self): 
	self.response.headers['Content-Type'] = 'text/html'
	self.response.write('<h5>You found the secret page!</h5>') 

class ViewPage(webapp2.RequestHandler):
  def get(self):
    view_template = the_jinja_env.get_template('templates/view.html')
    memes_result = Meme.query().order().fetch()
    variable_dict = {
      "memes": memes_result
    }
    self.response.write(view_template.render(variable_dict))

# the app configuration section	
app = webapp2.WSGIApplication([
  #('/', MainPage),
  ('/', EnterInfoHandler),
  ('/hello', MainPage),
  ('/secret', SecretPage),
  ('/results', ResultsPage),
  ('/view', ViewPage),
  ], debug=True)
