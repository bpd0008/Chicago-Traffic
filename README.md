# Chicago Traffic Accident App

##
This web app created a machine learning model from the City of Chicago's data portal. It estimates the mostly likely type of crash damage and possibility of a hit and run based on the user input route. The model incorporates time of day, day of the week, geolocation and enviornmental factors. User input is run through the model and then creates a accident profile by comparing it to similar accident data.

## Machine Learning Model 

The model relies upon the XGBoost python model. XGBoost stands for extreme gradient boost and employs a gradient boosted tree in its model. The three main predictors for damage and hit and runs were geolocation, lighting conditions and weather conditions. These enviormental factors impacted the model more than day or hour of route. The model had a 51% accuracy for damage type and 73.4% for hit and run profile.

## APP Design

The app was hosted on heroku at https://chicago-accident.herokuapp.com/ using flask. The app incorporated the code from https://github.com/jkgiesler/parse-chicago-neighborhoods/blob/master/gps_to_neighborhood.py to help with locating user routes from user address. Using google maps and the flask-googlemaps module the lat and long of the start and end route were calculated and run through the model. The output code was written directly in the data.html file using flask and jinja.