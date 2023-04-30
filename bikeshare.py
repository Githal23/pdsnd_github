import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
cities = ('Chicago', 'New York City', 'Washington')
months = ('All', 'January', 'February', 'March', 'April', 'May', 'June')
days = ('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
user_decisions = ('Yes', 'No')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input('Would you like to see data for Chicago, New York City or Washington?\n').title()
            if city in cities:
                break
            else:
                print('\nWrong city provided.\nTry again.\n')  
                 
    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('Which month? (all, january, february, ... , june)\n').title()
            if month in months:
                break
            else:
                print('\nWrong month provided.\nTry again.\n')  
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Which day? (all, monday, tuesday, ... sunday)\n').title()
            if day in days:
                break
            else:
                print('\nWrong day provided.\nTry again.\n')  
     
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_the_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        
        # filter by day of week to create the new dataframe
        df = df[df['day_of_the_week'] == day.title()]
        

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    common_month = df['month'].mode(1)[0]
    print('\n The most common month was:', common_month)

    # display the most common day of week   
    
    common_day = df['day_of_the_week'].mode()[0]
    print('\n The most common day of the week was:', common_day)

    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\n The most common hour was:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    common_start = df['Start Station'].mode()[0]
    print('\nThe most commonly start station was:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nThe most commonly end station was:', common_end)

    # display most frequent combination of start station and end station trip
   
    df['common_start_end'] = df['Start Station']+[' and ']+df['End Station']
    common_start_end = df['common_start_end'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip:', common_start_end)
    df.pop('common_start_end')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_days = int(df['Trip Duration'].sum()//86400)
    total_travel_time_hours = int(df['Trip Duration'].sum()%86400//3600)
    total_travel_time_minutes = int(df['Trip Duration'].sum()%3600//60)
    total_travel_time_secondes = int(df['Trip Duration'].sum()%3600%60)
    
    print('\nTotal travel time is eaqual', total_travel_time_days, 'days', total_travel_time_hours, 'hours', total_travel_time_minutes, 'minutes', total_travel_time_secondes, 'seconds')

    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()/60).round(2)
    print('\nMean travel time is eaqual', mean_travel_time, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('\nCounts of user types:\n', user_types_counts)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        no_gender_data = df['Gender'].isnull().sum()
        print('\nCounts of gender:\n', gender_counts, '\nNo data', no_gender_data)
    except: print('\nNo data availible for genders')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode()[0])
        print('\nUser year of birth stats:\nEarliest year of birth:', earliest_yob, '\nMost recent year of birth:', most_recent_yob, '\nMost common year of birth:', most_common_yob)
    except: print('\nNo data availible for birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data for 5 next rows."""
    
    # Ask user if raw data should be display
    row_number = df.shape[0]
    pd.set_option('display.max_column', None)
       
       
    for i in range(0,row_number,5):
        user_decision = input('\nDo you want to see the raw data? (5 next rows). Write Yes or No\n').title()
        if user_decision == 'Yes':
            data = df.iloc[i:(i+5),:].T            
            print('\n ', data)
            continue
        elif user_decision != 'Yes' and user_decision != 'No':
            print('\nWrong answer')
            continue
        else:
            break
            
                           
    print('-'*40)         
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
