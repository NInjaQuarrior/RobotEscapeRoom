# Robot Escape Room v3 23-24
Team Members: Iain McEwen, Connor McKevitt, Kaelin Panneton

## Project Description 
This is the robot repository for the **2023/24 Robot Escape Room v3** Major Qualifying Project (MQP) at WPI. The project encapsulates two programs, an escape room designer and the escape room website. The designer (found in NOTEX) allows a user to create the layout and components of a room and create a puzzle progression. The escape room website (found in Final_Robot_Website) takes a python file and then communicates how the physical room will interact while displaying the output from the robot's camera. The python files for the room pieces are found in Final_Room.


## How to Run: Designer
Run Final_Designer/web_stream.py

## How to Use: Adding a new room component to the Designer
Technical knowledge of how the piece you plan to add works is required for step 5(ii). 
1. Keep in mind the following: does this go in place of a floor piece or a wall piece, and is it an input or output? 
2. Get two PNGs, and ensure they are named the same as the piece you are adding  
    1. Get a picture of the piece as it will appear, either a picture or 3d render is recommended. This should be saved to "static/img/pieces". 
	2. Get a symbol that visually represents the piece, it should be simple in detail and easily viewable when shrunk down. This should be saved to "static/img". 
3. In roomLayout.js: 
    1. Add the name of the piece to the variable floorTypes or wallTypes as appropriate. 
	2. Add the dimensions of the PNG from step 2(i) to the variable natImages in the following manner: "piece name": [width, height]. 
4. In htnp.js: 
    1. Add the name of the piece to the variable inputs or outputs as appropriate. 
5. In finalProduct.js: 
    1. Add the dimensions of the PNG from step 2(i) to the variable natImages as you did in step 3(ii) 
	2. Add the following information to the variable conversions in the form "CapitalizedPieceNameWithNoSpaces":{topic:"5(ii)(a)", setup:"5(ii)(b)", initialState:"5(ii)(c)", activateMessage:"5(ii)(d)"}. Any unnecessary variables should be set to null. 
	    1. What topic the pi subscribes to when it starts. 
		2. The value the pi takes in to be properly initialized. 
		3. A command that tells the pi what physical state to start in. 
		4. A command that tells the pi what to do when activated. 


## How to Run: Escape Room
1. Connect to the Wi-Fi named escaperoom 
2. In Settings – Wi-Fi – change adapter options -> network connections - Wi-Fi - properties - ipv4 - Use following ipv4 address: 192.168.1.33 and set subnet mask to 255.255.255.0 
3. Turn on the robot 
4. Plug in pieces of the room
5. Run Final_Robot_Website/web_stream.py
6. Open a new command prompt in the file directory containing RobotControllerMQTT.py 
    1. Run command: python RobotControllerMQTT.py 