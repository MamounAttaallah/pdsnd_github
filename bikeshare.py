import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def validate_input(prompt, valid_options):
    """
    Validates input from the user.
    
    Args:
        prompt (str): The input prompt message.
        valid_options (list): The list of valid input options.

    Returns:
        str: A valid user input.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from {', '.join(valid_options)}.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    city = validate_input("Please choose a city (chicago, new york city, washington): ", CITY_DATA.keys())

    # Get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = validate_input("Please choose a month (january, february, ... , june) or 'all' for no filter: ", months)

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = validate_input("Please choose a day (monday, tuesday, ... , sunday) or 'all' for no filter: ", days)

    print('-'*40)
    return city, month, day

def filter_by_month(df, month):
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    return df

def filter_by_day(df, day):
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    df = filter_by_month(df, month)
    df = filter_by_day(df, day)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is: {most_common_month}")

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"The most common day is: {most_common_day}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"The most common hour is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " ->>>- " + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print(f"The most frequent trip is: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds.")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        counts_of_user_types = df['User Type'].value_counts()
        print("Counts of user types:")
        print(counts_of_user_types)
    else:
        print("User Type data is not available.")

    # Display counts of gender
    if 'Gender' in df:
        counts_of_gender = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(counts_of_gender)
    else:
        print("\nGender data is not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest year of birth:", earliest_year)
        print("Most recent year of birth:", most_recent_year)
        print("Most common year of birth:", most_common_year)
    else:
        print("\nBirth Year data is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """Displays raw data in increments of 5 rows upon user request."""
    print("\nDisplaying raw data...\n")
    start_row = 0
    while True:
        show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if show_data == 'yes':
            end_row = start_row + 5
            print(df.iloc[start_row:end_row])
            start_row += 5

            if start_row >= len(df):
                    print("No more raw data to display.")
                    break
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
