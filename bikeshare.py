import time
import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = input('Please enter a city from: chicago, new york city, washington: ').lower()
            CITY_DATA[city]
            break
        except KeyError:
            print('\n' + 'Not a valid city! Input one from the list shown.')
        finally:
            print('\nAttempted Input', '\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please enter a single month from january to june, or type all: ').lower()
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
            months.index(month)
            break
        except ValueError:
            print('\n' + 'Not a valid month! Input one from the list shown.')
        finally:
            print('\nAttempted Input', '\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please enter a day of the week, or type all: ').lower()
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            days.index(day)
            break
        except ValueError:
            print('\n' + 'Not a valid day! Input one from the list shown.')
        finally:
            print('\nAttempted Input', '\n')


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe by calling the city value from the dict
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract day of week from Start Time to create new columns
    df['day of week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # filter by supplied month to create the new dataframe
        df = df[df['Start Time'].dt.month_name() == month.capitalize()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.capitalize()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if month = 'all', otherwise print msg stating month they chose
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    comm_month = df['Start Time'].dt.month_name().mode()[0]
    if df['Start Time'].dt.month_name().nunique() == 1:
        print('You selected', comm_month.capitalize(), 'as your report month')
    else:
        print('The most common month for hiring a bike is...', comm_month.capitalize())

    # display the most common day of week, only if day = 'all'
    comm_day = df['day of week'].mode()[0]
    if df['day of week'].nunique() == 1:
        print('You selected', comm_day.capitalize(), 'as your report day of week')
    else:
        print('The most common day for hiring a bike is...', comm_day.capitalize())


    # display the most common start hour
    if df['Start Time'].dt.hour.mode()[0] <= 12:
        comm_hour = str(df['Start Time'].dt.hour.mode()[0]) + 'am'
    else:
        comm_hour = str(df['Start Time'].dt.hour.mode()[0] - 12) + 'pm'
    print('The most common hour for hiring a bike is...', comm_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)
    time.sleep(2)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    comm_sstat = df['Start Station'].mode()[0]
    print('The most commonly used start station is...', comm_sstat)

    #display most commonly used end station
    comm_estat = df['End Station'].mode()[0]
    print('The most commonly used end station is...', comm_estat)

    #display most frequent trip
    df['Start-End Station'] = df['Start Station'] + ' ..to.. ' + df['End Station']
    comm_trip = df['Start-End Station'].mode()[0]
    print('The most common trip is...', comm_trip)

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)
    time.sleep(2)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    tot_trav_time = df['Trip Duration'].sum()
    tot_trav_time_days = round(tot_trav_time/60/60/24,1)
    print('The total travel time of all rides is...',  tot_trav_time_days, 'days.')

    #display mean travel time
    mean_trav_time = df['Trip Duration'].mean()
    print('The average ride time is...', round(mean_trav_time/60,1), 'minutes.')

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)
    time.sleep(2)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    usercnt = df.groupby(['User Type'])['User Type'].count()
    for index, value in usercnt.items():
        print('User Type:', index, '| Count:', value)

    #Display counts of Gender
    if "Gender" in df:
        gencnt = df.groupby(['Gender'])['Gender'].count()
        for index, value in gencnt.items():
            print('Gender:', index, '| Count:', value)
        print('\n')
    else:
        print('No Gender data in data set')

    #Dispaly stats about Birth Years of users
    if "Birth Year" in df:
        earl_by = int(df['Birth Year'].min())
        late_by = int(df['Birth Year'].max())
        comm_by = int(df['Birth Year'].mode()[0])

        print('The earliest birth year is...', earl_by)
        print('The most recent birth year is...', late_by)
        print('The most common birth year is...', comm_by)
    else:
        print('No Birth Year in data set')

    print("\nThis took %s seconds." % round((time.time() - start_time),2))
    print('-'*40)
    time.sleep(2)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        i = 0
        while raw_data.lower() == 'yes':
            for i in range(i, i+5, 1):
                datadict = df.drop(labels='Start-End Station',axis=1).rename(columns={'Unnamed: 0': 'Trip ID'}).iloc[i].to_dict()
                for k, v in datadict.items():
                    print (k.capitalize() + ':', v)
                print('\n')
            i += 5
            raw_data = input('\nWould you like to see 5 more lots of raw data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break
        print('\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nGoodbye!')
            break

if __name__ == "__main__":
	main()
