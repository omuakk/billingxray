I am thrilled to submit my Final Project for CS50: Billing X-Ray.
Note that the site is live at www.billingxray.com !!

File orientation:
1. application.py is the Python script using the Flask framework that runs the website
2. SQL Files beginning "with PROD_" restructure the data from the CMS files (see link at the bottom)
3. index.html is the main page
4. layout.html controls the layout
5. results.html generates the resulting data for the physician to view his or her claims
6. npierror.html is the apology page if the NPI number is invalid

Additional background--

I've worked in the healthcare industry for over seven years. My partner, sister, father and number of friends are all physicians. Coming from a finance background, I am usually quite inquisitive about how physicians interact with the system and particularly how they view "money stuff". They're all smart people with more than enough intellectual capacity to undeerstand what's going on, but more often than not, the institutions they work for are either unable or unwilling to provide detailed financial information that can help them understand how they're being paid and why. This is becoming a more and more important issue as payers (both government and private) are starting to alter payments based on measures of performance, in an attempt to change physicians' behaviors. But how can they use reimbursement structure to change behavior if physicians have very little visibility into how they're being paid?

Billing X-Ray is my first attempt at helping solve this issue. CMS (The Centers for Medicare and Medicaid Services) have clearly gone through great lengths to make reimbursement data publicly available. However, I found the data, while thorough, fairly inaccessible particularly to a busy physician - I would much rather have them care for patients than digging through data! First, CMS separaates the databases by year, making it difficult to compare across years. Second, it's not straightforward to combine into a single "headline" number, to show the total billing for a particular year. Billing X-ray solves both of these problems.

I also really wanted to learn how to use AWS, so I used this as an opportunity to give myself a crash-course in the insanely powerful cloud platform to get the web app live. The good people at CS50 are right to advise against using AWS as too complex for a beginner: it did take quite a bit of time to get up and running, but I couldn't help myself!

Technically, the process I followed is:
1. I downloaded the data from the CMS website to my local machine (link below)
2. I uploaded it to an S3 bucket
3. I then created an RDS database using AWS Aurora running mySQL to house the database
4. I wrote the SQL scripts (SQL files included in the Project directory) to bring the data in from S3, and bring them all together into one file
5. I used Cloud9 on AWS (thank you CS50 for teaching that!)
6. The application is written in Python using the Flask framework, which connects to the database and displays the data for the NPI number requested (with an apology for an invalid number)
7. The front-end is constructed with Bootstrap
8. The application is deployed on Elastic Beanstalk
9. Note that each search is recorded in RDS with a timestamp so I can track usage!

It's already become a bit of a parlor game - my physician friends love using it to see how they compare vs. colleagues. They like to point out that it is quite incomplete as it only captures Government Administered Medicare (excluding Medicare Advantage and private payers) but it spurs the right conversations.

I hope someday I have the opportunity to build software to help physicians navigate the business of medicine!



CMS data: https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Physician-and-Other-Supplier.html
