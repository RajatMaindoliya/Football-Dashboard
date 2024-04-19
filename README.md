# Football-Dashboard
The primary objective of this project is to develop a live football analytics web application with a robust predictive modelling component, leveraging machine learning algorithms to forecast match outcomes.

## # Requirements
asgiref==3.7.2
certifi==2023.11.17
charset-normalizer==3.3.2
Django==5.0.1
idna==3.6
joblib==1.3.2
numpy==1.26.4
pandas==2.2.1
python-dateutil==2.9.0.post0
pytz==2024.1
requests==2.31.0
scikit-learn==1.3.0
scipy==1.13.0
six==1.16.0
sqlparse==0.4.4
threadpoolctl==3.4.0
tzdata==2023.4
urllib3==2.1.0

## # Step 1
Clone the repository:
> gh repo clone RajatMaindoliya/Football-Dashboard

## # Step 2
Create a virtual environment if you wish:
> python3 -m venv venv

## # Step 3 
Navigate to the MainProject folder:
> cd MainProject

## # Step 4
Apply migrations:
> python manage.py makemigrations
> python manage.py migrate

## # Step 5
Run the server
> python manage.py runserver