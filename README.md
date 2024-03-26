# training-data

python3 -m venv venv

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

export FLASK_APP=app.py

export FLASK_ENV=development  # Sets the environment to development, which enables debug mode

flask run

python app.py

#To run request.py

open a new terminal 

source venv/bin/activate

python request.py