
# FeedbackForm 2.0

This is a simple program to register anonymous and quick feedbacks from community during events.

## Install
To start using this program, wire your Raspberry Pi and open a terminal (either via SSH or physically opening it.

### Dependencies
First of all we have to install Pip3 and Git
```bash
sudo apt install python3-dev git
```
And the library used
```bash
sudo pip3 install gpiozero
```

We installed it as a sudoers because we use a CRON job to start it at startup

Now let's clone the project
```bash
git clone https://github.com/gdgpisa/feedbackform2.git
```
Let's move into the project directory
```bash
cd feedbackform2
```
and run the program
```bash
sudo python3 mainff.py
```


### Extra
You could choose to run it at startup, if this is your case, open a shell in your Raspberry Pi and then
```bash
sudo crontab -e
```
and add this line at the end of the file
```bash
@reboot cd /home/pi/feedbackform2 && /usr/bin/python3 /home/pi/feedbackform2/mainff.py
```

If you cloned the repo in a folder different from the home of the Pi account, you should change the paths.