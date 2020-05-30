import pickle


credentials = {
    "thingname": "",
    "endpoint": "",
    "pathname": ""
}

credentials['thingname'] = input("Enter your thing-name (as registered on AWS): ")

credentials['endpoint'] = input("Enter the AWS Broker endpoint: ")

credentials['pathname'] = input("Enter the pathname to <.../>connect_device_package/")


pickle.dump(credentials, open("connection.pkl", "wb"))

print("Done installing, run this script anytime to update connection credentials!")
