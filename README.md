Greenphire Lottery
===
Project:    Greenphire Lottery  
Author:     Sean Sissman  
Email:      seansissman@gmail.com  
Version:    1.0.1  
License:    GNU GPLv3  
Main:       greenphire.py  
Python:     3.4.3  


Description
---
Collect favorite numbers for Powerball tickets.  Accomplish this with the following requirements:


- Capture the name of the employees entering the number.
- The first 5 favorite numbers will need to be in the range of 1 to 69 and unique. (remember that this is a drawing so there cannot be duplicates in this range of 5 numbers)
- 6th favorite number will need to be in the range of 1 to 26 and flagged as the 6th Powerball number.
- Keep count of each individual favorite number provided to determine which numbers to use in our final winning number. (ie count the duplicates).
- Retrieve the max count of each unique duplicate number and use them as the powerball numbers.
- if there is a tie based on the max counts randomly select the tied number.
- Display all employees with their corresponding number entries.
- Display the final powerball number based on the requirements above.

Sample output:
```
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
```


Installation
---
Only standard Python libraries are used, therefore only Python 3.4 is required for the environment.

Three files are required.  Place them into your project directory:
-  greenphire.py
-  lottery.py
-  greenphire_lottery.cfg


Usage
---
In a terminal, from the project directory run:
`python greenphire.py`

**Options:**
```
 -p, --prompt       Prompt if user would like to repeat.
 -r, --repeat       Automatically rerun the script.
 Note:  If multiple options are entered (ie. -p -r), -p will take priority.
```

During the initial execution a file named `favorite_numbers.db` will be created.  This file stores the history of the numbers entered as an SQLite database.
To clear this history, simply delete the file.

Configurations can be made in `greenphire_lottery.cfg`.  Default configs are set for project requirements, but can be reconfigured for a different lottery.  
**Note**:  If changing the number of favorite numbers to be selected, you will also need to adjust the number of printing placeholders in the `Output` section.  You should also change the file configured under the `SQL` section or delete the existing file.


To Do / Additional Notes
---
- [ ] Requirements included sample output.  Within this sample output the prompts for the 4th and 5th favorite numbers do not include closing parenthesis `)`.  Confirm with the client if this is a typo or an actual requirement.
- [ ] Some terminals automatically echo a newline after input is provided with the `input()` function, displaying an extra line between prompts.  Per the sample output, not all prompts are followed by a blank line.  Ask client if this is acceptable.


