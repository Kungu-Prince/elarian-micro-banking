
                                           Mwananchi Bank
Description:
Mwananchi Bank is a simple banking application built with Python and Flask, integrated with MongoDB for data storage. The application provides basic banking functionalities such as checking balance, transferring money, applying for loans, enrolling in SACCO, and more.

Features:
•	Check balance
•	Transfer money
•	Withdraw funds
•	Lipa na meBank (payment feature)
•	Table banking
•	Apply for loans
•	Enroll in SACCO


Prerequisites:
Technologies:
•	Python 3.x
•	MongoDB Atlas account
•	Africa's Talking account (for SMS functionality)


Installation:
       Clone the repository:
       
         https://github.com/Kungu-Prince/elarian-micro-banking.git
         
  Navigate to the project directory:
    bash
    
          cd API BANKING
          
  Install dependencies
    
           pip install -r requirements.txt
  
Set up environment variables:
Create a .env file in the root directory.
Add the following environment variables:
 Run this in your command prompt terminal where your project is in for its  environ variables to be saved
makefile

      MONGODB_URI=<your_MongoDB_URI_here>
     AFRICASTALKING_USERNAME=<your_AfricasTalking_username_here>
      AFRICASTALKING_API_KEY=<your_AfricasTalking_API_key_here>

Run the application:

      python app.py

Usage:
Access the application through the /ussd endpoint via POST requests.
Use a tool like Postman or cURL to send requests to the endpoint with the required parameters.
Follow the USSD prompts to interact with the banking functionalities.

Contributing:
Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements:
•	MongoDB Atlas
•	Africa's Talking

Contact:
For any inquiries or support, please contact   princekungu8@gmail.com
