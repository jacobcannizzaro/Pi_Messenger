# Pi_Messenger

## 

### Setting up:

1. Create a directory for this project, for reference I call outer directory `pi-mess`

2. Clone this repo into directly into `pi-mess`

3. 

4. Ask Jake to download your device package for you. You will get a file: `connect_device_package.zip`

5. Unzip downloaded file:

   `$ unzip connect_device_package.zip`

6. You should now have four files:

   1. `<thing-name>.cert.pem`
   2. `<thing-name>.private.key`
   3. `<thing-name>.public.key`
   4. `start.sh`

   Put these four files in one folder `connect_device_package/` and place this folder directly into `pi-mess` as well so that your directory structure looks like:

   ```
   pi-mess/
   	|____Pi_Messenger/
   	|____connect_device_package/
   ```

   

   (Note: NEVER upload your .pem or .key files to a public git repo!!! This is why these files are not present in this repo and the reasoning behind the directory structure given above)

7. Check for / download dependencies and libraries needed:

   ```
   $ openssl version
   OpenSSL 1.1.0f  25 May 2017
   $ python3 --version
   Python 3.7.7
   $ sudo pip install paho-mqtt
   $ sudo  apt-get update
   ```

   Note: python and openssl should already be installed on the Raspberry-Pi 4 model b. This step is just making sure of that. These libraries do work with Python 2.7 but this project is using Python 3. Pip is a package installer  for python libraries, and if say for instance pip installing paho-mqtt appears to work but then when you run your python3 instance and import it, the compiler says it cannot find the library, then try installing again using `sudo pip3 install...`

8. Go to (cd into) `connect_device_package/` directory and run following commands:

   ```
   $ pip install AWSIoTPythonSDK
   $ chmod +x start.sh
   $ ./start.sh
   ```

   This downloads an AWS python SDK, gives execute permissions to the `start.sh` file, and then runs that file. Running `start.sh` will populate your directory with a `root-CA.crt` certificate file.

9. Before running anything, let's set up your thing-policy. It's default configuration only allows subscriptions to the AWS test broker during the test that is run after configuration in the `start.sh` file. Change your devices policy (force Jake to change it) to: 

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "iot:Publish",
           "iot:Subscribe",
           "iot:Connect",
           "iot:Receive"
         ],
         "Resource": [
           "*"
         ]
       }
     ]
   }
   ```

   This will allow the publishing and subscribing to the channels used in `chat.py`

10. Now everything should be set up in your directory and on AWS's side of things (AWS is playing the role of the Broker), so let's run the installation script:

    Begin by changing into the `Pi-Messanger/src/` directory and then run

    ```
    $ python3 install.py
    ```

    This will prompt you to enter three things, your thing-name, host endpoint (broker address), and a pathname to your `connect_device_package/` directory. The output will appear as follows:

    ```
    Enter your thing-name (as registered on AWS): jakepi
    Enter the AWS Broker endpoint: a1wrobr8i9l833-ats.iot.us-east-1.amazonaws.com
    Enter the pathname to <.../>connect_device_package/: ../../
    Done installing, run this script anytime to update connection credentials!
    ```

    Note: You must change "jakepi" to whatever your thing-name is. If you've followed these instructions correctly thusfar, the pathname will be the same as well, and the broker endpoint is the same for all of us. As the script states, if you mess up entering this information you can simply re-run the install script.

    This will add `connection.pkl` to your src directory.
    This is necessary as it holds your connection information.

11. Now you are ready to chat! 

    From within the same (`src/`) directory, you can now run:

    ```
    $ python3 chat.py
    ```

    As long as someone else is chatting you are now ready for a dandy ol' time.

    Otherwise it's like shouting into a valley with no echoes :(

    Have fun.
