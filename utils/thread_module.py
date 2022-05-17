# -*- coding: Utf-8 -*-
# Module that contain the thread used in app
import threading as th
from multiprocessing import Process, Pipe
from models.database_basics import connect

class QueryThread(th.Thread):
    "A thread option that will process the queries in another thread"
    def __init__(self, query: str,  func= None):
        th.Thread.__init__(self)
        self.query= query   # The query
        self.done= 0    # The done flag
        self.result= [] # Result variable
        self.func= func # Function list
        return
    def run(self):
        con, cur= connect()
        # Create user defined functions if the parameter allows it
        if self.func != None:
            for function in self.func:
                con.create_function(function[0], function[1], function[2])  # Name, arg number, reference
        
        cur.execute(self.query) # Execute the query
        
        self.result= cur.fetchall()  # Getting the result in self.result
        self.done= 1    # Mark that the querying is done

        # Close connection
        cur.close()
        con.close()
        return
###############################################################################################################################################################
class QueryProcessor(Process):
    "A try of the Process version"
    def __init__(self, sender, query, function_list= None):
        Process.__init__(self)
        self.result= sender # Will send the databases results
        self.query= query
        self.functions= function_list
    def run(self):
        con, cur= connect()
        if self.functions != None:
            for function in self.functions:
                con.create_function(function[0], function[1], function[2])  # Name, arg number, reference
        
        cur.execute(self.query)
        self.result= cur.fetchall()
        
        #self.sender.send(self.result)
        
        # Connection closing
        cur.close()
        con.close()