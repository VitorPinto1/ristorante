# ristorante
ristorante

Prerequisites

-	Visual Studio Code
-	Extension Python pour VS Code
-	Git
-	Python 3.9
-	Flask
-	Mailtrap

1.	Installation and Deployment

Launch VSCode and install the "Python" extension published by Microsoft. After creating the folder, open an integrated terminal in VS Code to clone the repository and execute the following commands:

	« git clone https://github.com/VitorPinto1/ristorante.git »
	« cd ristorante »

2. 	Environment Configuration

Activate the Python virtual environment in the terminal:

	« source env/bin/activate »  # Unix ou MacOS
	« env\Scripts\activate »    # Windows

Install the required packages using requirements.txt:

  « pip install -r requirements.txt » 

3. 	Launching the Application

Run the application with Flask in the terminal:

	« python app.py »
	« flask run »

4. 	Accessing the Application

Open your browser and go to:
	
 	http://127.0.0.1:5000/

To view emails, open your browser and go to:

	-https://mailtrap.io/home
  
You will need your Mailtrap user credentials.

Conclusion

By following these steps, you should be able to deploy the web application locally and test its functionalities.