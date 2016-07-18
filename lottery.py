import sqlite3
import operator
from collections import Counter
import traceback
import random


class Lottery(object):
    """ Generic lottery object """

    def __init__(self, **lottery_config):
        # Define Lottery instance attributes with custom data types
        self.name = lottery_config['name']
        self.count = int(lottery_config['count'])
        self.min_number = int(lottery_config['min_number'])
        self.max_number = int(lottery_config['max_number'])
        self.unique_numbers = lottery_config['unique_numbers']
        self.bonus_number = lottery_config['bonus_number']
        if self.bonus_number:
            self.bonus_name = lottery_config['bonus_name']
            self.min_bonus_number = int(lottery_config['min_bonus_number'])
            self.max_bonus_number = int(lottery_config['max_bonus_number'])
            self.bonus_unique = lottery_config['bonus_unique']

        # Placeholder for new numbers
        self.favorite_numbers = []

        # Placeholders for database columns and data
        self.db_cols = ''
        self.db_data = []


    def get_favorite_numbers(self):
        """ Returns favorite_numbers list"""
        return self.favorite_numbers


    def get_num_count(self):
        """ Returns total number of numbers needed to play """
        if self.bonus_number == 'True':
            return self.count + 1
        else:
            return self.count


    def has_bonus_num(self):
        """ Returns 'True' is lottery uses a "bonus" number """
        return self.bonus_number


    def set_numbers(self, prompt_config, **kwargs):
        """ Prompts user for favorite numbers with prompts declared in 
            prompt_config
        """
        exclusions = ''
        while len(self.favorite_numbers) < self.count:
            if len(self.favorite_numbers) > 0:
                exclusions = ' excluding ' + self.format_exclusions(
                                self.favorite_numbers)
            # Create prompt_string with format defined in config file
            prompt_string = prompt_config.format(
                selection = kwargs['ordinal'](len(self.favorite_numbers) + 1),
                min = self.min_number,
                max = self.max_number,
                exclusions = exclusions,
                padding = ' '          # right padding
            )
            # Prompt for a favorite number based on Lottery type and
            # previous selections.
            try:
                new_fav_num = int(input(prompt_string))     # Prompt for num
            except ValueError:
                print('Bad input type!  Please select an integer.')
                continue
            if new_fav_num < self.min_number or new_fav_num > self.max_number:
                print(('{} is out of range!  Please select a different '
                       'number.').format(new_fav_num))
                continue
            elif self.unique_numbers == 'True':    # If numbers must be unique
                if new_fav_num in self.favorite_numbers:   # If not unique
                    print(('{} has already been selected!  Please select a '
                           'different number.').format(new_fav_num))
                    continue
            self.favorite_numbers.append(new_fav_num)   # Append valid num
        if self.bonus_number == 'True':
            self.set_bonus(prompt_config)


    def set_bonus(self, prompt_config):
        """ Prompts user for bonus number with prompts declared in
            prompt_config
        """
        # Create prompt_string with format defined in config file
        prompt_string = prompt_config.format(
                            selection = self.bonus_name,
                            min = self.min_bonus_number,
                            max = self.max_bonus_number,
                            exclusions = '',    # no exclusions
                            padding = ' '     # right padding
                            )
        while True:
            try:                
                bonus_num = int(input(prompt_string))
            except ValueError:
                print('Bad input type!  Please select an integer.')
                continue
            if bonus_num < self.min_bonus_number or \
                bonus_num > self.max_bonus_number:
                print(('{} is out of range!  Please select a different '
                       'number.').format(bonus_num))
                continue
            self.favorite_numbers.append(bonus_num)
            break


    def format_exclusions(self, favorite_numbers):
        """ Returns a formatted string listing numbers to be excluded """
        exclusion_list = [str(i) for i in favorite_numbers]
        size = len(exclusion_list)
        if size == 1:
            return exclusion_list[0]
        elif size == 2:
            return exclusion_list[0] + ' and ' + exclusion_list[1]
        else:
            exclusions = ''
            for i in range(len(exclusion_list) - 1):
                exclusions = exclusions + exclusion_list[i] + ', '
            return exclusions + 'and ' + exclusion_list[-1]


    def execute_sql(self, db, *statements):
        """ Executes the SQL statement """
        conn = sqlite3.connect(db)
        c = conn.cursor()
        for statement in statements:
            c.execute(statement)
        conn.commit()
        conn.close()
            


    def add_to_history(self, db, *args):
        """ Adds the new favorite numbers to the database.
            arg_columns include columns to add to db
            besides the favorite numbers (eg. first and last name).
        """
        
        # Create a string for additional columns based on *args
        for arg in args:
            for k, v in arg.items():
                self.db_cols = self.db_cols + k + ', '
                self.db_data.append(v)
        
        # List of strings for header names for lottery numbers
        if self.bonus_number == 'True':
            num_headers = ['num_{!s}'.format(x) 
                            for x in range(1, self.count + 2)
                            ]
        else:
            num_headers = ['num_{!s}'.format(x) 
                            for x in range(1, self.count + 1)
                            ]
    
        # String for column names for each data field (args and numbers)
        columns = self.db_cols + ', '.join(num_headers)
        
        # String of column names to create table (includes PK)
        create_col = 'id INTEGER PRIMARY KEY AUTOINCREMENT, ' + columns
    
        # SQL statement to create table
        create_table = 'CREATE TABLE IF NOT EXISTS {table} ({col});'.format(
                            table=self.name,
                            col=create_col
                            )
    
        # SQL statement to add a new row of lottery numbers
        new_row = 'INSERT INTO {table} ({col}) VALUES {data};'.format(
                            table=self.name,
                            col=columns,
                            data=tuple(self.db_data + self.favorite_numbers)
                            )
        
        # Execute SQL (create table and add row)

        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute(create_table)     # Create table if none exists
            c.execute(new_row)          # Insert new row with new numbers


    def get_history(self, db):
        """ Query the database for relevant history """
        
        # SQL query retrieving all rows from lottery table in reverse order
        get_all = 'SELECT * FROM {table} ORDER BY id DESC;'.format(
                        table=self.name
                        )
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute(get_all)     # Query *
            all_rows = c.fetchall()

        return all_rows
        
    def get_drawing(self, db=None, all_history=None):
        """ Returns lottery drawing results based on historical counts """

        # If historical selections are not provided, get from db
        if not all_history:
            if not db:      # If DB not provided
                raise TypeError('No data provided to calculate drawing in:  ' +
                                    'Lottery.get_drawing()')
            all_history = self.get_history(db)

        # Single list of historical numbers (just numbers, no other columns)
        flat_nums = [j for i in all_history
                        for j in i[len(self.db_cols.split(',')):]]

        # Create separate lists of standard nums and bonus nums
        standard_nums = []
        bonus_nums = []
        for i in range(len(flat_nums)):
            if self.has_bonus_num():        # If lottery has bonus number
                if (i+1) % (self.count+1) != 0:     # Skipping bonus num index
                    standard_nums.append(flat_nums[i]) # Append standard num
                else:
                    bonus_nums.append(flat_nums[i]) # Append bonus num
            else:                       # If lottery does not have bonus num
                standard_nums = flat_nums

        # Create Counter objects (dictionary like {number:count}) for each 
        # favorite number
        standard_counts = Counter(standard_nums)
        bonus_counts = Counter(bonus_nums)
        
        # Create list of tuples based on (k,v) of Counters that will be 
        # sorted by v.
        sorted_std_counts = sorted(standard_counts.items(), 
                                   key=operator.itemgetter(1)
                                   )
        sorted_bns_counts = sorted(bonus_counts.items(), 
                                   key=operator.itemgetter(1)
                                   )
 
        # Create list of most common numbers for drawing excluding the nth
        # most common where n is the final number ie. 5th out of 5        
        std_draw = [x[0] for x in sorted_std_counts[(self.count -1) * -1 :]]
        
        # Append final number to list, which is randomly chosen from all
        # numbers with that count        
        std_draw.append(self.handle_tie(sorted_std_counts, 
                                        index=self.count * -1))
        
        # Select bonus number which is randomly chosen from all numbers with
        # the highest count
        bns_draw = self.handle_tie(sorted_bns_counts, index=-1)
  
        return std_draw + [bns_draw]
        
        
        
    def handle_tie(self, nums, index):
        """ Returns a random selection of highest count favorite number if 
            there is a tie.
        """
        candidates = []
        count = nums[index][1]

        try:
            while nums[index][1] >= count and abs(index) <= len(nums):
                candidates.append(nums[index][0])
                index-=1
        except IndexError:
            pass

        return random.choice(candidates)