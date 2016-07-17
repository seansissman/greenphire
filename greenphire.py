import lottery
from configparser import RawConfigParser, ExtendedInterpolation


CONFIG_FILE = "./greenphire_lottery.cfg"


def get_config(section):
    """ Returns a dict of options from the CONFIG_FILE for section """

    config_parser = RawConfigParser(interpolation=ExtendedInterpolation())
    config_parser.read(CONFIG_FILE)
    config = {}
    for option in config_parser.options(section):
        try:
            config[option] = config_parser.get(section, option)
        except KeyError:
            config[option] = None
    return config


def ordinal(num):
    """ Returns ordinal number string from int, e.g. 1, 2, 3 becomes 1st, 2nd,
        3rd, etc.
    """
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}

    # Handles numbers that end in 11th, 12th, 13th
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # Default is 'th'
        suffix = suffixes.get(num % 10, 'th')
    return str(num) + suffix


def main():

    # Prompt user for name
    prompts_config = get_config('Prompts')
    first_name = input(prompts_config['first_name'].format(''))
    last_name = input(prompts_config['last_name'].format(''))

    # Create Lottery object with Powerball attributes from config
    lottery_config = get_config('Lottery')
    pb = lottery.Lottery(**lottery_config)

    # Prompt user and set favorite numbers
    pb.set_numbers(prompts_config['favorites'], ordinal=ordinal)

    # Get new favorite numbers
    favorite_numbers = pb.get_favorite_numbers()

    # Add row to SQL database
    if favorite_numbers:
        db = get_config('SQL')['numbers']
        pb.add_to_history(db, {'first_name': first_name},
                              {'last_name': last_name})

        # Retrieve and print all history
        all_history = pb.get_history(db)
        history_format = get_config('Output')['history']
        print()     # one blank line
        for row in all_history:
            print(history_format.format(*row[1:]))  # Skip index 0 (ID)

        # Print message for Powerball drawing
        drawing_message = get_config('Output')['drawing_message']
        print('\n' + drawing_message.format(pb.name.capitalize(), ''))

        # Select and print numbers for drawing
        drawing_nums = pb.get_drawing(db)
        drawing_results = get_config('Output')['drawing']
        print(drawing_results.format(*drawing_nums))


if __name__ == '__main__':
    main()