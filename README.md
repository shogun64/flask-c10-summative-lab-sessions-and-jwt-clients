# Summative Lab 10

All code is contained within the 'client-with-sessions' folder - the client-with-jwt folder has been unaltered.

The endpoints for login, signup, logout, and check session function as intended - however, the journal and journal/<id> endpoints do not, as the frontend has not been properly built to accommodate them.

For the former, follow the setup instructions below after cloning the repository:

```bash
cd client-with-sessions
pipenv install
pipenv shell
cd server
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python3 seed.py
export FLASK_APP=app.py
flask run --port=5555
```
After opening a new terminal:
```bash
cd client-with-sessions
npm install
npm run start
```
The browser page should open automatically.