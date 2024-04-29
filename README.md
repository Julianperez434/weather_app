# WEATHER APP

# Table of Contents
- [WEATHER APP](#weather-app)
- [Table of Contents](#table-of-contents)
- [Description](#description)
  - [Overview](#overview)
- [File Structure](#file-structure)
  - [app.py](#apppy)
  - [Templates](#templates)
    - [layout.html](#layouthtml)
    - [login.html](#loginhtml)
    - [register.html](#registerhtml)
    - [dashboard.html](#dashboardhtml)
    - [history.html](#historyhtml)
    - [board.html](#boardhtml)
    - [settings.html](#settingshtml)
    - [success.html](#successhtml)
  - [Static](#static)
    - [style.css](#stylecss)
  - [Instance](#instance)
    - [weather.db](#weatherdb)
- [Functionality](#functionality)
  - [Login and Registration](#login-and-registration)
    - [Registration](#registration)
    - [Login](#login)
  - [Dashboard](#dashboard)
  - [History](#history)
  - [Board](#board)
  - [Settings](#settings)
- [Design Choices](#design-choices)
  - [Flask Framework](#flask-framework)
  - [SQLite Database - SQLAlchemy](#sqlite-database---sqlalchemy)
  - [Bootstrap Framework](#bootstrap-framework)
  - [External API](#external-api)
- [Future Improvements](#future-improvements)
  - [Better Design](#better-design)
  - [Error Handling](#error-handling)
  - [Settings Module](#settings-module)
- [Conclusion](#conclusion)


# Description

## Overview
This Weather App is a simple web application that allows users to check the weather of any city in the world. Users can register, log in, and view their search history. There is also a message board where users can post and view messages. The app is built using HTML/CSS/JavaScript/Bootstrap for the frontend, and Python with Flask for the backend. SQLite with SQLAlchemy is used to handle the database.

> IMPORTANT: The app requires an API_KEY, you need to use your own key as enviromental variable.

> export API_KEY='your_api_key'

# File Structure
The main folder for this app is called 'project', there you can find the main app.py.
>cd project/

## app.py
This is the main Flask application. Here it defines all the routes and their functionalities, including login, registration, dashboard, history, board, settings, and logout.

## Templates
This folder contains all the HTML templates and a single layout used to render the pages of the application.

### layout.html
A basic layout structure with Jinja templating, the navigation links along with the Bootstrap, CSS, and JavaScript head links.

### login.html
The template for the login module, where the user can input their credentials.

### register.html
The template for the register module, is where the user can register a username, email and password.

### dashboard.html
The template for the dashboard, once the user is logged in, they can access this page, this is the place for the main functionality of this app.

### history.html
The template for the history tab, the user can see a log of their past searches.

### board.html
The template for the board. Here is where messages from any user can be seen.

### settings.html
The template for settings. It is the page where users can customise their experience or change their password.

### success.html
A helper template to show feedback to the user when the registration is successful.

## Static
A folder with a single helper file.

### style.css
Here is a simple CSS file to change the appearance of the HTML templates on top of Bootstrap.

## Instance
This folder contains the SQLite database.

> The database schema is included in the code and created automatically.

### weather.db
The database for the app.

# Functionality

## Login and Registration

### Registration
This module is handled with the register.html template. Users can register using these fields:

>Username, Email, Password, Confirm password

The username has to be unique, the email requires basic formatting, and both passwords have to match. There is a basic input handling built-in both for frontend and backend.

If the user fails to pass any validation, then the page redirects again to the register page plus a customised alert in flask based on the validation failed.

When the user passes all the validation, then the app renders the success.html template where a message shows that the app has successfully registered the user in the database. After 10 seconds the user is redirected to the login page using a simple JavaScript script.

### Login

This module is simpler than registration, using a connection to the database through SQLAlchemy queries it checks if the user exists and also if their password matches with the one registered in the database.

> An important feature is that all the passwords are hashed and stored in that way.

Again, if the user fails to pass, an alert from Flask is shown when redirected to the login page. The alert gives the user feedback about what they did wrong.

## Dashboard
Once logged in, users are redirected to the dashboard where they can search for the weather data of any city. This app fetches data from an external API [Ninja API] and displays it to the user in different human-readable formats.

The API documentation can be found here:

> https://api-ninjas.com/api/weather

The dashboard consists of an input field where the user can search for their city. Based on the result, the app displays the result with a background colour depending on the temperature, the rest of the data is shown in a table.

> This app is responsive thanks to Bootstrap, it looks good on any device. Take in account that it's optimized for larger screens.

From the dashboard page, the user can see their name on the right-top of the page, where the navigation bar is shown because the user has been logged in.

Any successful search is inserted into the database history table.

## History
Here the user can see a table sorted by date with any past search. It only registers the city, the temperature and the timestamp.

> This can be useful if the user has lost their internet connection, at least can take a look at some cached information.

To obtain this data, this modulo gets the information from the history table, then using a loop renders this information into a bootstrap table.

## Board
Here users can post messages on a message board. This board is shown to all users. Messages are stored in the database and retrieved on this page.

>Messages are shown in order from last sent to first sent

Board and history tables are responsive both horizontally and vertically.

## Settings
Users can change their password by entering their current password and a new password. If the current password matches with the one registered on the database, the new password is updated on the database.

> In this module the passwords are still being hashed

# Design Choices
This project was chosen because is not too complex but at the same time requires a foundation of several technologies, so is in a good spot to be both reasonable for a solo developer while challenging on their own.

## Flask Framework
Flask is a no-brainer for a solo app, it's simple and flexible, allowing us to build an app like this with Python. Also, Flask's session management is perfect for handling user authentication and maintaining user sessions through different pages of the application.

## SQLite Database - SQLAlchemy
This database is lightweight and simple and is suitable for a small-scale application like this one. SQLAlchmey simplifies the workload once one gets a grasp of its syntax.

## Bootstrap Framework
Bootstrap was used for the frontend to ensure a quick, clean, and responsive design. It's a bit of a tradeoff with some flexibility lost.

## External API
Ninja Weather API is a known server on the web that can be used to fetch weather data.


# Future Improvements
## Better Design
The app has room to improve its frontend design. As mentioned before, bootstrap is a trade-off for a quick, clean and responsive app with less room for a customised design.

## Error Handling
With more expertise, we could implement a more robust error handling and provide better feedback to users in case of invalid inputs.

## Settings Module
The settings module was meant to be the entry point where users could customise their experience, something like changing the colour theme or even a dark mode is difficult to achieve through Bootstrap.
> Using CSS or SCSS we could create color variables. Bootstrap comes with a built-in SASS variable list but it requires a deeper knowledge of the framework.

# Conclusion

This Weather App is a simple yet functional web application to check the weather of any city. It comes with a user-friendly interface and essential features such as login, registration, search history, and message board.
