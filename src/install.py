import pickle

#initialize dictionary
credentials = {
    "thingname": "",
    "endpoint": "",
    "pathname": ""
}

#fill dictionary with user input
credentials['thingname'] = input("Enter your thing-name (as registered on AWS): ")

credentials['endpoint'] = input("Enter the AWS Broker endpoint: ")

credentials['pathname'] = input("Enter the pathname to <.../>connect_device_package/: ")

#save this dictionary's state by pickling it
pickle.dump(credentials, open("connection.pkl", "wb"))

print("Done installing, run this script anytime to update connection credentials!")
