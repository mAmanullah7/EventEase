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


