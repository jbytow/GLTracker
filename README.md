# GLTracker
GLTracker is webb application for DESKTOP usage developed for my household to keep tracking diet I'm on as the excel food log I've prepared wasn't good enough. 

## Features

* Food List: List of either default (data scrapped by myself from: https://glycemic-index.net/) or added by users products with their macronutrients and glycemic load per 100g
* Meals: Creating meals from items from Food List, counting and viewing their details such as macronutrients and glycemic index&load
* Food Log: Log to keep tracking of what was eaten each day vs Daily Requirements set by user, can add both Meals and food Items, also has macronutrients breakdown
* Profile: User profile that's also weight history vs target weight and shows user data such as BMI

## Using APP
App is accessible at: https://www.gltracker.eu/, either you can make own account or user testuser:
login: testuser
password: TeSt135!

## Test Coverage
75% based on coverage.py report

## Built With
* Python
* Django
* Django Select2
* Django REcaptcha
* HTML
* CSS
* Bootstrap
* Javascript
* JQuery

## Installation on local
1. Clone the Repository
```bash
git clone -b master https://github.com/jbytow/GLTracker.git
```

2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Set up .env file with:
* SECRET_KEY
* EMAIL_HOST_USER
* EMAIL_HOST_PASSWORD
* RECAPTCHA_PUBLIC_KEY
* RECAPTCHA_PRIVATE_KEY

5. Run Migrations
```bash
python manage.py migrate
```

6. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to http://127.0.0.1:8000/ to see the application in action.
    
## License

[MIT](https://choosealicense.com/licenses/mit/)
