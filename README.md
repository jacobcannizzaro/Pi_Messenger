# Secure Encrypted Pi Messenger (SEMPi)

## 

### Overall Idea:

​	How often have you been trying to revolt against arbitrary oppression and had no way to securely communicate with your comrades? The answer, if you are like us, is all too often. This project's goal is to create your own private, secured, and *free* messaging application. The *free* aspect is possible thanks to AWS's IoT Core & free tier. AWS has a free tier for the first year after creating a new account, so after the year, just go through this process again. More pricing information can be found: https://aws.amazon.com/iot-core/pricing/. 

​	This project takes advantage of AWS's private MQTT broker. MQTT is a publish/subscribe messaging protocol commonly used for IoT devices. AWS's broker is inherently secure as uses TLS to ensure confidentiality of the protocol. This means it will generate a package of keys (public & private) as well as a trusted certificate. This ensures that no party without the keys and certificate could connect to the broker. This ensures secure machine-to-machine (M2M) communication. However, while this means no outside party could access the broker, the broker is being run on AWS. AWS could become the real-life Skynet so we don't really want them to be able to read our messages either. Therefore we add end-to-end encryption on the client side of the application, secured with a session key. This allows users who wish to chat with eachother the opportunity to come up with a session key that they agree upon and that only they know. With this, the broker never has the plain text messages available, and only the encrypted text. Therefore, even if a hacker somehow broke into your system and stole your private keys and certificate, they wouldn't be able to read unencrypte messages without that session key.

### Setting up:

1. Create a new AWS account (can use your old one if you have one but creating a new one leaves no doubt that you have one year of the free tier).

2. Once in the main AWS dashboard, click on 'Services' and find 'IoT Core'.

3. Once at the main 'AWS IoT' page, click on 'Onboard' -> 'Get started'. 

   1. Then hit the blue 'Get started button' under "Onboard a device".
   2. Then click 'Get started' in the bottom right.
   3. Click 'Linux/OSX' under 'Choose a platform'.
   4. Click 'Python' under 'Choose a AWS IoT Device SDK'
   5. Click 'Next'.
   6. Give your thing a name and click 'Next step'
   7. Click to download your connection kit for Linux/OSX.
   8. Continue with the next step of this tutorial and leave the window with the command line instructions open but don't follow them yet (later running `./start.sh` will populate this window with testing output) . We will get to those steps in this tutorial. Continue to the next step.

4. Create a directory for this project, for reference I call outer directory `pi-mess`

5. Clone this repo into directly into `pi-mess`

6. After downloading your connection kit, you will get a file: `connect_device_package.zip`

7. Unzip downloaded file:

   `$ unzip connect_device_package.zip`

8. You should now have four files:

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

9. Check for / download dependencies and libraries needed:

   ```
   $ openssl version
   OpenSSL 1.1.0f  25 May 2017
   $ python3 --version
   Python 3.7.7
   $ sudo pip3 install paho-mqtt
   $ sudo pip3 install PyCrypto
   $ sudo  apt-get update
   ```

   Note: python and openssl should already be installed on the Raspberry-Pi 4 model b. This step is just making sure of that. These libraries do work with Python 2.7 but this project is using Python 3. Pip is a package installer  for python libraries, and if say for instance pip installing paho-mqtt appears to work but then when you run your python3 instance and import it, the compiler says it cannot find the library, then try installing again using `sudo pip3 install...`. 

10. Go to (cd into) `connect_device_package/` directory and run following commands:

   ```
   $ pip3 install AWSIoTPythonSDK
   $ chmod +x start.sh
   $ ./start.sh
   ```

   This downloads an AWS python SDK, gives execute permissions to the `start.sh` file, and then runs that file. Running `start.sh` will populate your directory with a `root-CA.crt` certificate file.

11. Before running any python files, let's set up your thing-policy. It's default configuration only allows subscriptions to the AWS test broker during the test that is run after configuration in the `start.sh` file. You can edit your thing's policy by going to 'Secure' on the left hand side of the IoT Core dashboard, and then to policies, clicking the respective thing's policy. Click edit and change your devices policy  to: 

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

    This will allow the publishing and subscribing to the channels used in `sempi.py`

12. Now everything should be set up in your directory and on AWS's side of things (AWS is playing the role of the Broker), so let's run the installation script:

    Begin by changing into the `Pi-Messanger/src/` directory and then run

    ```
    $ python3 install.py
    ```

    Note: I did not have to install the python library `pickle` on my Pi, but if there is an error relating to this that arises when running this script, then try `pip install pickle-mixin` or `pip3 install pickle-mixin` if that doesn't work. May need to run with root priviledge (i.e. add `sudo` at the beginning).

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

13. Now you are ready to chat! 

    From within the same (`src/`) directory, you can now run:

    ```
    $ python3 sempi.py
    ```

    Click the connect button, enter a session key, and as long as someone else is chatting you are now ready for a dandy ol' time.

    Otherwise it's like shouting into a valley with no echoes :(

    Have fun. Stay safe. We do not promote illegal activity of any kind. 
