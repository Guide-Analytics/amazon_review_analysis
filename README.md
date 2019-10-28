
## Gide Product Analysis: (macOS Only - not ready for Windows)

Welcome to Gide Product Analysis! This is a small-beta platform where you will be entering a website URL that contains product reviews. 

As of now, we currently only support Amazon sites. 

There will be 2 outputs for now (there will be more outputs in the future as we utilize Machine Learning algorithm).


**Make sure you are on Python 2.7 (technically the syntacies formatted to work on Python 3.6 and above, but just on the same side)**
**Will continue source code to Sublime Text (Eclipse Sucks!)**


**What you will need for testing and library requirements:**

Mike’s installation further notes 2.1.2 / Minh's edit patch 2.0


**To get a python script writer:**

* Pycharm (Recommended for now): "The professional IDE for professional developer" https://www.jetbrains.com/pycharm/download/#section=mac (Current version: 2018.3.4)


**For server and database running:**

* Postgres Installation (server/port calling): https://postgresapp.com
* PSequel Installation (recommended for better viewing the database): http://www.psequel.com


**Creating the environment for your compiler:**

* Create virtualenv for 2.7, use the original installing point.

	* Python (on mac) potential installing point: 

		* Run: which python; to know where is your python located
		
	* Open terminal, and activate virtual environment (virtualenv) from above:

	* Install Homebrew: 

		* Run: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	* Install pip, pip2, pip2.7, but not 3:

		* Run: sudo easy_install pip

	* Install virtualevn: 

		* Run: sudo -H pip install -U virtualenv

	* Install the python through virtualenv:

		* Navigate through Terminal to where you wishes to install virtualenv

		* Run: Virtualenv -p (where_your_python_is_located) (virtualenv_name)

		* To activate: 

			* Run: source (virtualenv_name)/bin/activate

		* To deactivate:

			* Run: deactivate


**Necessary libraries and other extra support:**

* Libraries installation:

	* Open terminal, and activate virtual environment (virtualenv) from above:

	* Install Homebrew: 

		* Run: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	* Install pip, pip2, pip2.7, but not 3:

		* Run: sudo easy_install pip

	* Install psycopg2, for SQL: (2.7.6.1 is the latest that the system can recognize)

		* Run: sudo -H pip install -U psycopg2

		*NOTE: Possible error: clashes libssl against ssl from Python, refer to: http://initd.org/psycopg/docs/

	* Install Universally Unique id:

		* Run: sudo -H pip install -U uuid

	* Install Date unitalities to grab essential time stamp for the data:

		* Run: sudo -H pip install -U python-dateutil

	* Install Selenium and it should support 2.7 and 3.4+:

		* Run: sudo -H pip install -U selenium

	* Install DateTime to extract out: 

		* Run: sudo -H pip install -U DateTime

	* Install Regex: (https://docs.python.org/2/library/re.html) – more functionality and other stuff:

		* Run: sudo -H pip install -U regex 
		*(you may not need to install this as Python contains a standard package called: re)

	* Install nltk, for tokenization:

		* Run: sudo -H pip install -U nltk

	* Install matplotlib, for prereq for numpy installation:

		* Run: sudo -H pip install -U matplotlib

	* Install numpy, in case the original python installation does not have sufficient libraries:

		* Run: sudo -H pip install -U numpy 
			*Installing Numpy may cause issues as it overlaps with pandas. 
			*If the error message contains numpy already existed in pandas with the latest version, you can ignore the installation process 
			*Otherwise, run: sudo -H uninstall numpy Then, run: sudo -H install -U numpy

	* For panda plot – visualization and data frame: 

		* Run: sudo -H pip install -U pandas

	* Sci-Py: for scientific calculation

		* Run: sudo -H pip install -U scipy

	* Built more upon Matplotlib and Numpy and Scipy:

		* Run: sudo -H pip install -U scikit-learn

	* Calculate all statistical value needed:

		* Run: sudo -H pip install statistics

	* Sentiment score calculation:

		* Run: sudo -H pip install -U "watson-developer-cloud>=2.4.1"

	* Create backend handling for our scrapper:

		* Run: touch ~/.matplotlib/matplotlibrc

		* Run: open ~/.matplotlib/matplotlibrc

		* Type in that file: “backend: TkAgg” without the quotation marks and close the file

	* This is for something, … we just forgot why, ask mike for this:

		* Run: sudo -H pip install -U textblob

	* Run Python:

		* Run: python

		* Run: import nltk

		* Run: nltk.download(“punkt”)

		* Run: nltk.download(“stopwords”)

	*You can choose to close the virtualenv here, since we are done by deactivating it, or just leave it on if you’re about to use it


**Let’s get this started:** 

* Run Postgres:

	* Go in server settings, use port 5433

	* Name can be whatever

	* Click run, then leave it aside

* Run Psequel to have database for Selenium.

	* Open Psequel

	* Details: 

	* Host: localhost

	* User: postgres

	* Pass: *nothing here

	* Database: postgres

	* Port: 5433

	* Click Connect

* FOR NOW: copy GideProductAnalysis file from “https://bitbucket.org/GideAdmin/gide-mvp/src/master/GideProductAnalysis/”

* Open terminal, and let’s run this:

	* Activate virtualenv:

		* Locate your way to the GideProductAnalysis
	
	* Run: python \_\_init\_\_.py

	* Follow instruction on the file for more details.

* Refresh Psequel for the updated result

**Underlying method of Operation:(No idea what this's doing here)** 

*Phase 1: Scraping website reviews:*

* Under microservice *SeleniumAnalysis* (note: *Extraction* is part of the *SeleniumAnalysis* microservice)

*Phase 2: Extraction and push to database:*

* Under microservice *Extraction* and microservice *Database* 
* This is where the program extract words and sentences from database.

*Phase 3: Database tables viewing:*

* Under microservice *Database* (This is a very small package). Hostname: *localhost*, user: *postgres*, port: *5433*
* We can see five columns: author_table, review_table, product_table, wordslabelling, sentencelabelling 
* (sentencelabelling will be removed as wordslabelling mimics wordslabelling)

*Phase 4: Filtering reviews in database through rules and variables:*

* Under microservice *FilteringAnalysis* 
* This is where all the reviews are being calculated by the rules given. 
* This microservice allows rules to analyze word count usage, quality of words used, sentiment scores for each review, repeated review analysis, verified purchasers, 

*Phase 5: Machine learning training models:*

* Under microservice *MLAnalysis*
* We are using LinearDiscrimantAnalysis to simple match and categorize author's scores (a better output, only if it's for a general purpose - simpler to read)
* We are also using K-MeansNeighbours to match rigourously and categorize approximately to author's scores (a better output, but only if trained data are labelled correctly)
* Lastly, (not implemented until the future), we use Logistic Regression to better filter the bad and good reviews from the output dataset. 


**Important note**

*Selenium:*
	
* When installing Selenium, we recommend installing WebDriver for Firefox (Firefox WebdDriver). 
* The file name is called: geckodriver-v0.xx.0-macos (https://github.com/mozilla/geckodriver/releases)
* Once the download has finished, please move the executable file to folder: /usr/local/bin (otherwise, the program won't run!!)

*General Note:*

* Everytime you want to scrape new reviews from sites, there will be a reset/override of the previous score data. Otherwise, the program won't run. 
* It will be best. if you have multiple URLs to scrape when considering putting them onto the database. 	
* Once new data are in the database, and you want to calculate the scores for machine learning preparation, make sure to set the scores to 0: "Score reset:" N (as there are no scores to be reset anyways). 
* This ensures score columns are being created. 

**Syncronization:**
Pull and setup on Bitbucket:

*In PyCharm:*

* Go: "VCS" -> "Checkout from Version Control" -> "Git"	
* Url: https://bitbucket.org/GideAdmin/gide-mvp/src/master	
* Select Ok*
* To get files from bitbucket, click "Update Project"
	*It will show file differents and ask for syncronization*
* To push what you have up, click "Commit"
	*Pycharm will show the file updated and will ask for commit message*
	*Include name and time for verification*

*In Eclipse:*
	
* In Eclipse, go to "File" > "Import" > "Git" > "Projects from Git" > "Clone URI" 	
* Enter the following information: URI = "https://bitbucket.org/GideAdmin/gide-mvp/src/master", user and password is the Bitbucket login information
	Click "Next", then ensure "master" is checked and click "Next" again, double check the directory and click "Next Again", and then click "Finish"
* Now in the menu bar, look under "Window" > "Perspective" > "Open Perspective" > "Other" > "Resource" and click "Open"
* Now in the meny bar, look under "File" > "Import" > "Git" > "Projects from Git" > "Existing local repository" < "Select a Git Repository" > "Import as General Project" > "Next" > "Finish"

Run StartAnalyze __init__.py to start analysis on desire page. GLHF.

Firstly, you will be prompted as to whether you want to extract, filter, both, or do both AND give a report. The parameters are: 'e', 'f', 'b', 'r'.
If somehow you want to do both, *FilteringAnalysis* will prompt you if you want to reset the scores. You will need to enter: N

*Extraction:*

The URL has to contain the following format: 
*https://www.amazon.ca/'product-name'/product-reviews/'product-id'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1*
The **&pageNumber=x** must be included for the program to run. You will be prompted to enter the number of seconds of loading time 
(I suggest 5 seconds; this gives the website some time to load or else you'll be caught as a bot. 

*FilteringAnalysis:*

After being prompted to reset the score, the program will do the work; Review Sentiment analysis will take sometime as it is loooking every single sentence in all the reviews.