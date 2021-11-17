# Fetch Rewards

## Coding Challenge

### Instructions to run program

1. From the terminal at the root of this repository, run the following command to ensure that the necessary libraries are available in your local environment

```bash
pipenv install
```

2. From the terminal at the root of this repository, run the following command to ensure that the flask environment will have the necessary information to run

```bash
export FLASK_APP=index.py
```

3. From the terminal at the root of this repository, run the following command to start the flask server to handle the associated routes

```bash
pipenv run flask run
```

4. From here you can use either postman or another program that allows users to send HTTP requests to urls to test the app. The flask app will be running on localhost:5000 as a default, so the base url for the following routes is http://localhost:5000/.

-   POST /add-points
-   POST /spend-points
-   GET /points-balance
