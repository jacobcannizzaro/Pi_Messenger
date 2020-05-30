# Pi_Messenger

### Setting up our first example:

Follow this for video walkthrough: https://www.youtube.com/watch?v=Q-UujfueMZ8

Follow this link for the detailed steps that goes along with the video: https://www.apdaga.com/2018/02/install-aws-amazon-sdk-on-raspberry-pi.html

1. Ask Jake to download your device package for you. You will get a file: `connect_device_package.zip`

2. Unzip downloaded file:

   `$ unzip connect_device_package.zip`

3. You should now have four files:

   1. `<thing-name>.cert.pem`
   2. `<thing-name>.private.key`
   3. `<thing-name>.public.key`
   4. `start.sh`

   Put these four files in one folder `connect_device_package/`
   (Note: NEVER upload your .pem or .key files to a public git repo!!!)
4. Check for / download dependencies and libraries needed:

   ```
   $ openssl version
   OpenSSL 1.1.0f  25 May 2017
   $ python3 --version
   Python 3.7.7
   $ sudo pip install paho-mqtt
   $ sudo  apt-get update
   ```

   Note: python and openssl should already be installed on the Raspberry-Pi 4 model b. This step is just making sure of that. These libraries do work with Python 2.7 but this project is using Python 3. Pip is a package installer  for python libraries, and if say for instance pip installing paho-mqtt appears to work but then when you run your python3 instance and import it, the compiler says it cannot find the library, then try installing again using `sudo pip3 install...`

5. Go to `connect_device_package/` directory and run following commands:

   ```
   $ pip install AWSIoTPythonSDK
   $ chmod +x start.sh
   $ ./start.sh
   ```

   This downloads an AWS python SDK, gives execute permissions to the `start.sh` file, and then runs that file. Running `start.sh` will populate your directory with a `root-CA.crt` certificate file.

6. Download `aws_iot_pub.py` & `aws_iot_sub.py` from this repository and then allow execute permissions for them:

   ```
   $ chmod +x aws_iot_sub.py
   $ chmod +x aws_iot_pub.py
   ```

7. If you tried to run these files now, you will get an error because the AWS policy for your "thing/device" has not been set up. It's default configuration only allows subscriptions to the AWS test broker during the test that is run after configuration in the `start.sh` file. Change your devices policy (force Jake to change it) to: 

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

   This will allow the publisher to publish to and the subscriber to subscribe to the channels used in `aws_iot_sub/pub.py`

8. Before using these programs, you must go into both files and replace every instance of `jakemacbook` with whatever your devices name is.

9. To see this example in action, open two terminal windows. In the first, run:

   `python3 aws_iot_sub.py`

   In the second window, run:

   `python3 aws_iot_pub.py`

10. You should now see temperature messages flowing from the publisher to the broker and getting recieved by the subscriber. Good luck! Feel free to open issues in the repo if you are unclear about any aspect of this.
