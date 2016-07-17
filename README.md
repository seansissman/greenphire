Greenphire Lottery
===



Description
---

Collect favorite numbers for Powerball tickets.  Accomplish this with the following requirements:

'''
Capture the name of the employees entering the number.
The first 5 favorite numbers will need to be in the range of 1 to 69 and unique. (remember that this is a drawing so there cannot be duplicates in this range of 5 numbers)
6th favorite number will need to be in the range of 1 to 26 and flagged as the 6th Powerball number.
Keep count of each individual favorite number provided to determine which numbers to use in our final winning number. (ie count the duplicates).
Retrieve the max count of each unique duplicate number and use them as the powerball numbers.
if there is a tie based on the max counts randomly select the tied number.
Display all employees with their corresponding number entries.
Display the final powerball number based on the requirements above.

Sample output:
Enter your first name: Wade
Enter your last name: Wilson
select 1st # (1 thru 69): 12
select 2nd # (1 thru 69 excluding 12): 20
select 3rd # (1 thru 69 excluding 12 and 20): 23
select 4th # (1 thru 69 excluding 12, 20, and 23: 56
select 5th # (1 thru 69 excluding 12, 20, 23, and 56: 30
select Power Ball # (1 thru 26): 25

Wade Wilson 15 26 33 60 34 powerball: 16
Frank Castle 15 26 34 56 61 powerball: 16

Powerball winning number:
15 26 34 55 63  powerball: 16
'''

Installation
---
Only standard Python libraries are used, therefore only Python 3.4.3 is required for the environment.

Three files and one directory are required:
-  greenphire.py
-  lottery.py
-  greenphire_lottery.cfg
-  /data


Use
---
In a terminal, from the project directory run:
'python greenphire.py'

