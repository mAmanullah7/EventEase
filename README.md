### Instructions to Run the Application

- Install all required Python modules from `requirements.txt` using the command:
  ```
  pip install -r requirements.txt
  ```
- After successful installation of the required modules, run the `main.py` file using the following command:
  ```
  python main.py
  ```
- The app will be accessible at: `http://127.0.0.1:5000`. Use this URL to access the web application.
- To run the API, refer to the `EventEase_api.yaml`.




### Folder Structure

- `admin`: Contains the Flask Blueprint app supporting admin functionality for the web application.
  - `admin_application`: Python files related to admin functionality.
  - `admin_templates`: Folder containing HTML and Jinja templates for the admin frontend.
  - `admin_bp.py`: Blueprint for the admin application, defined in this Python file.
  
- `applications`: Contains Python files related to core application functionality.

- `static`: Contains static assets such as images and CSS files.

- `templates`: Contains HTML and Jinja templates for the user-facing part of the application.

- `main.py`: The main Python file for running the web application.

- `requirements.txt`: Contains a list of required Python modules for smooth application execution.


```|
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
+---eventease.sqlite3
+---eventease_api.yaml


