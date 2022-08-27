# -*- coding: Utf-8 -*-
# Creating a binary file to check if there is already a subscribed user
import configparser as cp   # A python module to help creating ini configuration files
import os

def create(db= '''db\management.db''', appstate= 0):
    "To create the Appstate configuration file with the path to the database and the active app tracker"
    config= cp.ConfigParser()  # ConfigParser to create the configuration file
    config['DEFAULT']= {
        'Database path': db,
        'Is active': appstate
    }
    
    # Configuration file creation
    with open('''app_state.ini''', 'w') as app_state:
        config.write(app_state)
        
###############################################################################################################################################################
def read():
    "to read the app_state.ini file"
    config= cp.ConfigParser()  # Create a ConfigParser object
    if not os.path.exists('''app_state.ini'''):# If the ini file is already present
        create()
    config.read('''app_state.ini''')
    # If the app_state is wrong, create
    if not ('DEFAULT' in config and 'Database path' in config['DEFAULT'] and 'Is active' in config['DEFAULT']):
        create()
    return str(config['DEFAULT']['Database path']), int(config['DEFAULT']['Is active'])
###############################################################################################################################################################