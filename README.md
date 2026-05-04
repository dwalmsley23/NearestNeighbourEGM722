# NearestNeighbour EGM722
This project is based on a nearest neighbour analysis 
for bus stops in Northern Ireland and creating a tool to find 
the nearest bus stop to each postcode. This is to fulfil the project
requirements for EGM722 at University of Ulster

## 1.Set Up and Installation.
1. To be able to access and use this code, you must download both Conda and
Git from the relevant websites online. [Conda](https://docs.conda.io/en/latest/) and [Git](https://gitforwindows.org/)
2. Create or log in to your GitHub account and fork this repository
(https://github.com/dwalmsley23/NearestNeighbourEGM722) into your own
account.
3. You should then clone the fork into your own account as this will allow you to
use and potentially edit the code as you deem necessary.
4. From the anaconda navigator app, use the import environment function to
import the environment.yml file contained within the repository that you have cloned. This will create a conda environment with associated dependencies
downloaded.
5. Having cloned the repository and created a conda environment, you should
be able to launch your choice of IDE to make use of the code. The author
used PyCharm in the creation of this code.


## 2. Troubleshooting
2.1 Using different data set
If you download a different data set to use for the NNA then you may need to amend
the code to ensure that the geodataframe is using the correct columns for the
latitude and longitude within the CSV file. If the locations are given in a different
projection then you may need to amend the epsg number. This can be found using
the following website https://epsg.io/. `


2.2 Time delay
The iterative process to find the closest bus stop for each bus stop in Northern
Ireland is the most time intensive element of the code. This will take several minutes
for a larger data set and there is no way to ascertain how far along the process the
program has reached so you need to employ patience.

2.3 Input of post code
You must ensure that the code is entered in the format BT7 3HE. There must be a
gap after the first three digits or 4 digits if there are 7 digits in the postcode eg BT23
7EF. The program cannot function if the postcode is entered incorrectly.