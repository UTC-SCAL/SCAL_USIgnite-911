"""
Author: Jeremy Roland
Purpose: Have some basic API calling methods that can be reused later, also some additional methods that convert the
    typical JSON formatted response to a DataFrame and csv file
"""
import requests
import json
import pandas


def apiCall404():
    """
    Purpose: Show a basic get() call and what it returns
    """
    response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")
    print(response.status_code)


def apiCallSpacePeopleCount():
    """
    Purpose: Make an API call to get the current number of humans in space
        Saves the response to a json file
    Since this endpoint we're requesting info from has no parameters, it's an easy call
    """
    response = requests.get("http://api.open-notify.org/astros.json")
    print(response.status_code)

    return response.json()
    # Save the json file to a json file
    # with open("../", 'w') as outfile:
    #     json.dump(response.json(), outfile)


def getISSPassTime():
    # This endpoint tells us the next time the ISS will pass over a specified GPS point
    # This endpoint requires lat/long parameters
    response = requests.get("http://api.open-notify.org/iss-pass.json", params={'lat': 40.71, 'lon': -74})
    # Print the status of our request, to make sure everything went ok
    print(response.status_code)

    return response.json()
    # Save our response as a dict
    # myResponse = response.json()
    # Print out the response to more easily view what we have
    # jPrint(myResponse)
    # Cut down our response to a particular directory in our dict
    # myResponseCut = response.json()['response']


def jPrint(obj):
    """
    Purpose: print a JSON file in a more easily readable format
    Note: I didn't make this, I took it from the internet
    """
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def flattenJSONTemplate(responseData):
    """
    Purpose: Flatten multiple directories in a dict (API response file), then append them together
        Meant to be used as a template for how the code should generally look
    """
    jPrint(responseData)
    # Based on the directory names seen from the jPrint method, change the column names below to flatten what you want
    flattenedData1 = pandas.json_normalize(responseData['column name'])
    flattenedData2 = pandas.json_normalize(responseData['column name'])
    # Print them out to double check everything's ok
    print(flattenedData1)
    print(flattenedData2)
    # Concat the flattened data together into a dataframe
    # The outer parameter leaves any empty rows as NaN
    result = pandas.concat([flattenedData1, flattenedData2], axis=1, join='outer')
    # Print your concated DF and save it as a csv
    print(result)
    result.to_csv("../", index=False)


# There are many types of API requests that we can make
# The most common is GET, which is used to retrieve data
# When making a request, the response from the API comes with a response code, telling us if the request was successful
# get() function returns a response object, which we can get info from
# apiCall404()
