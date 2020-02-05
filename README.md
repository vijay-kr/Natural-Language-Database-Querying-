# Natural Language Database Querying

Python web-application that levarages NLTK to enable business users to query their database in Natural Language (Speech or Text) and get Interactive Visualizations

**Vision behind this project**

Managers today need to make informed decisions in real time. Top companies use data-driven insights to make business decisons, and it is crucial to speeden up the process for managers and non-technical users to be able to fetch reuslts from their database quickly and efficiently. 

So we asked ourselves, what is the fastest and most efficient way to fetch results? *Google, of course!* Setting Google Search as the benchmark, our team of aspiring Business Analysts and Data Scientists set out to create an application where non-technical users can query their databases without any prioir technical knowledge or intervention by a data analyst.

*So now, why SQL? When you can Google*

**A quick walkthough**

Here's a quick demo of what our application does. *I highly recommend technical folks reading this to download the applicaition and try it out yourselves!*

**Search using voice or text:**

![Home Page Search](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/search.JPG)

**The results (yes! it's that simple):**

![Result](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/result.JPG)

*Please note that this version (v1) is just a proof of concept with limited functionalities. We invite you to expand upon it and help the community!*


**These are the python functionalities we leveraged to build this application:-**

![Python Functionalities](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/lib.JPG)


**Business Use-cases**

1. **Quick results for Managers & Clients:**
Reducing turnaround time to fetch results for non technical managers in product companies and clients in service based companies. Especially useful when outsourcing to foreign countries.

![Usecase 1](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/usecase1.jpg)

2. **Integrate with Chat-Bots:**
Enables customers to obtain answers to the common queries like product availability, prices, discounts, et al. Querying through these chatbots eliminates the need for technical analysts and reduces man-hours.

![Chatbots](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/chatbots-header.png)

3. **Improved Data Exploration for Analysts:**
Equips analysts with ready-to-consume reports for the data exploration, enabling them to make faster and easier analyses

![Visualizations](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/bg-showcase-3.jpg)


**Getting Started**

1. Download the database file 'csv_test10.db' from this link: https://drive.google.com/a/umn.edu/file/d/1NF1ZvYjsrjVFNT3EP4-XmhKt1vzsyF9L/view?usp=sharing
2. Save the above database file in the same folder as the application - "Natural Language Database Querying" 
3. Install the following Python Packages using "pip install <package_name>" : pandas, nltk, re, autocorrect, pygal, pygal_maps_world, sqlite3.
4. Run the application using the command "python nql.py"
5. Go to http://127.0.0.1:5000 from your web-browser.
6. Try out queries (speech or text) like:
   * What are my top 10 countries as per rev in 2011
   * What are my monthly sales in 2011

    (feel free to try spelling mistakes and other years such as 2010 which is there in the database)

You are free to play around with nql.py and modify it to query your own database in natural language.

**Feel free to get in touch for more information:** Harsh Seksaria / https://www.linkedin.com/in/harsh-seksaria/

**Team:** (L-R) Rekha Mohandass, Jashyant Sikhakholi, Harsh Seksaria, Vijay K Raghupati, Darshika Sharma

![Team](https://github.com/harshseksaria1/Natural-Language-Database-Querying/blob/master/Natural%20Language%20Database%20Querying/images/f.jpeg)

Location: Ovative Group, Minneapolis
