# MQP_Robot 
Team Member: Olivia Bell, Nathon Clune, Lillie DeHaemer, Liang Lu, Grace O'Reilly, Zachary Sarrett 

## Project Description 
This is the robot repository for the **2022/23 Robot Escape Room v2** Major Qualifying Project (MQP) at WPI. The project creates an interactive escape room where players controls the robot to escape. The project is consisted of three essential components: website, robot, and room. The player interacts throught the website, where the camera feed of the robot is streamed. The player uses the keyboard to navigate the robot across the rooms. 

## Files Description 
robot_move.py: file with move functions. </br>
robot_control.py: file with keyboard control. </br>
robot_variables.py: file with pin numbers (GPIO). </br>
robot_detect.py: file with ArUco detection for camera. </br>
web_stream.py: file with ArUco detection for camera and connection to website (flask). </br>
-- html files goes into templates folder </br>
-- js, css, images, etc. goes into static folder </br>
robot_mqtt_publish/subscribe.py: testing files for mqtt. </br>
** run robot_mqtt_publish.py and robot_mqtt_subscribe.py in separate terminals at the same time to test for mqtt. </br>

### Connecting a Computer to Raspberry Pi
*** Computer and Raspberry Pi should be connected to the same network. *** </br>
***ip address could be found using 'hostname -I' in terminal on Raspberry Pi*** </br>

#### For MAC, in terminal: </br>
-- *ssh pi@<ip_address>* (e.g. ssh pi@130.215.173.87) </br>
-- password: *escape* </br>
-- use 'exit' to quit </br>
** this connects to the terminal of raspberry pi; see Microsoft Remote Desktop for connecting to desktop </br></br>

#### For Windows: </br>
-- open **PuTTy** </br>
-- put in IP address as hostname </br>
-- port 22 </br>
-- make sure SSH is selected </br>
-- click open to connect </br>
** this connects to the terminal of raspberry pi, follow below steps to connect to remote desktop </br>
-- open Remote Desktop Connection </br>
-- enter IP address and connect </br></br>

#### Microsoft Remote Desktop: </br>
-- open Microsoft Remote Desktop </br>
-- choose add PC </br>
-- use IP address as PC name, and add </br>
-- *username:* pi </br>
-- *password:* escape </br></br>

#### Using Monitor: </br>
-- connect monitor with raspberry pi using hdmi cable </br>
-- connect keyboard and mouse directly to pi </br>
-- connect raspberry pi to power </br>
-- wait patiently for monitor to show desktop of raspberry pi </br>

## Running the Robot and the Website
In Terminator (or multiple terminal windows), run the following concurrently: </br>
sudo python3 robot_control.py (for robot) </br> 
python3 web_stream.py (for website) </br>
-- flask will tell you where it is running on, copy and paste the URL into a web browser for website </br>
-- you can also use *http://[host-ip-address]:port* to run the website </br>
&ensp;&ensp; -- where [host-ip-address] is the ip address where you are running web_stream.py on </br>
** you may have to use ***cd*** to change current directory to the wished file </br>
** sudo is used so keyboard module can be used </br>
-- robot_detect.py enables the camera to detect for ArUco. </br>
use *ctrl C* to exit </br>
** if *ctrl C* does not work, use *ctrl Z* to force stop </br>
use *esc* (customized) to exit robot_control.py -> where keyboard module is used. </br>

## Debug Corner 
**ISSUE #1:**</br>
from terminal: </br>
-- ssh: connect to host 130.215.173.87 port 22: Connection refused </br>

***potential solution:***</br> 
-- IP address changed </br>
-- in terminal: hostname -I </br>
-- ^^^ gives the IP address ^^^ </br>
-- need to connect to raspberry π server to find the new IP address (aka connect to monitor) </br></br>

**ISSUE #2:**</br>
from terminal: </br>
-- ssh: connect to host 130.215.173.87 port 22: Connection timed out </br>
-- internet issue... certificate issue... not able to install issue... </br> 

***potential solution:***</br> 
-- unstable wifi </br> 
-- ask IT Desk for help to connect to WPI-Wireless </br>
-- https://hub.wpi.edu/article/361/connect-to-wpi-wireless-using-a-raspberry-pi-with-gui </br>
-- ssh not enabled (either the pi or host computer) </br></br>

**ISSUE #3:**</br>
keyboard import error: you must be root to use this library on linux </br>

***potential solution:***</br>
-- run file from terminal using sudo </br>
-- see instruction from section *Running Robot* </br></br>

**ISSUE #4:**</br>
everything working, but camera not showing up on website </br>
error message: "AttributeError: module 'cv2.aruco' has no attribute 'DetectionParameters'" </br>

***potential solution:***</br>
-- in web_stream.py, comment out lines 79-82, and uncomment 74-74 </br>
-- on local computers, use line 79-82 for testing. </br></br>

**ISSUE #5:**</br>
cv2 error / camera issues </br>

***potential solution:***</br>
-- try "sudo reboot" to reboot the pi </br>
-- disabling debug mode for flask may resolve "Can't open camera by index" </br>
** commands below *may* only work with camera connected to the camera port (i.e. not usb camera) </br>
-- use "vcgencmd get_camera" to check if camera is detected </br>
-- use "raspistill -o test.jpg" to check if camera is detected </br></br>

**ISSUE #6:**</br>
ImportError: numpy.core.multiarray failed to import </br>

***potential solution:***</br>
-- cv2 cannot be imported when using sudo command </br>
-- move cv2 into a new file and run separately </br></br>

**ISSUE #7:**</br>
Port 8000 is in use by another program. Either identify and stop that program, or start the server with a different port.</br>

***potential solution:***</br>
-- use "kill -9 $(ps -A | grep python | awk '{print $1}')" </br>
-- "ps aux | grep web_stream" -> "kill *process id*" or "kill -9 *process id*" </br></br>
