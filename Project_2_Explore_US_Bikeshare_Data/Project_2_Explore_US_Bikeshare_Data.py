import time
import pandas as pd
import numpy as np

#datasets declaration
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #declaration of variables
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    month = input('Please write a month from January to June or write "all" to see all the months : ')
    
    # data collections city, months, days and hours
    city = input('From the following cities, select one and write it down, Chicago , New York City or Washington : ')
    city = city.casefold()
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = month.casefold()
    day = input('Write a day of the week or write "all" to see the whole week : ')
    day = day.casefold()
    
    #Data validation
    while city not in CITY_DATA:
        city = input('Invalid city name.Please Try Again!')
        city = city.casefold()
      
    while month not in months:
        month = input('Invalid month name.Please Try Again!')
        month = month.casefold()
       
    while day not in days:
        day = input('Invalid day name.Please Try Again!')
        day = day.casefold()
    
    print('='*40)
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

    #reading and extract the datasets in the dataframes
    df = pd.read_csv(CITY_DATA[city])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Month and day validation
    if month != 'all':        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':        
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #most popular month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    #Most Popular Day
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #Most Popular Start Hour:
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    

    print('most popular month:', months[popular_month-1])
    print('Most Popular Day:', days[popular_day])   
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    #most popular stations
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])
    print('Most Popular End Station: ', df['End Station'].mode()[0])
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
   
    #travel duration
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total Trip Duration:', df['Trip Duration'].sum())
    print('Mean Trip Duration:', df['Trip Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    #User Stats
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    
    print(user_types,'\n')
        
    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender,'\n')
        
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        print('Most Common year of Birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
    
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        enter = ['yes','no']
        user_input = input('Would you like to see more data? (Enter:Yes/No).\n')
        
        while user_input.lower() not in enter:
            user_input = input('Please Enter Yes or No:\n')
            user_input = user_input.lower()
        n = 0        
        while True :
            if user_input.lower() == 'yes':
        
                print(df.iloc[n : n + 5])
                n += 5
                user_input = input('\nWould you like to see more data? (Type:Yes/No).\n')
                while user_input.lower() not in enter:
                    user_input = input('Please Enter Yes or No:\n')
                    user_input = user_input.lower()
            else:
                break           
 
        restart = input('\nWould you like to restart? (Enter:Yes/No).\n')
        
        while restart.lower() not in enter:
            restart = input('Please Enter Yes or No:\n')
            restart = restart.lower()
        if restart.lower() != 'yes':
            print('BYE!')
            break

if __name__ == "__main__":
	main()