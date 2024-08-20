Instruction to run the applications

Install all the required python modules from requirement.txt using the following command pip install -r requirements.txt
After successfully installing the required modules, run main.py python file using the following command python main.py in command prompt.
App is running on http://127.0.0.1:5000. Use above url to access the web application.
In order to run api refer showspot_api.yaml
Folder Structure

admin: Flask Blueprint app running to support admin functionality for web application.
admin_application: Python applications related to admin functionality
admin_templates: Folder with html | jinja templates for frontend for admin functionality
admin_bp.py: Blueprint app running in this python file
appliations : stores application related python files
static: stores static files such as images, css files
templates: stores HTML and Jinja templates for frontend for user functionaliyt
main.py: main application file
requirements.txt: list required python modules necessary for smooth running of application
|
+---admin
|	+---admin_applications
|	|	+---admin_controllers.py
|	|	+---admin_login.py
|	+---admin_templates
|	|	+---admin_base.html
|	|	+---admin_homepage.html
|	|	+---admin_login.html
|	|	+---admin_newShow.html
|	|	+---admin_register.html
|	|	+---admin_register_confirmation.html
|	|	+---admin_venue_new.html
|	|	+---deleteShow_confirmation.html
|	|	+---deleteVenue_confirmation.html
|	|	+---edit_show.html
|	|	+---edit_success.html
|	|	+---edit_venue.html
|	|	+---show_added.html
|	|	+---summary.html
|	|	+---venue_added.html
|	+---admin_bp.py
+---applications
|	+---api.py
|	+---config.py
|	+---database.py
|	+---login.py
|	+---models.py
|	+---user_controller.py
|	+---validation
+---static
|	+---images
|	|	+---graphs
|	|	|	+---capacity_per_show.jpg
|	|	|	+---capacity_per_venue.jpg
|	|	|	+---revenue_per_show.jpg
|	|	|	+---revenue_per_venue.jpg
|	|	+---logo
|	|	+---venue_img
+---templates
|	+---base.html
|	+---book_show.html
|	+---booking_history.html
|	+---booking_success.html
|	+---cancel_successfully.html
|	+---home.html
|	+---index.html
|	+---register_confirmation.html
|	+---search_shows.html
|	+---search_venue.html
|	+---user_base.html
|	+---user_login.html
|	+---user_register.html
|	+---venue_details.html
+---main.py
+---readme.md
+---requirements.txt
+---showspot.sqlite3
+---showpsot_api.yaml
