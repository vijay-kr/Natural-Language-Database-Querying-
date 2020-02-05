from time import time
import pandas as pd
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import os
Base = declarative_base()

class Price_History(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'Price_History'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False) 
    invoiceno = Column(String)
    stockcode = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    invoicedate = Column(String)
    unitprice = Column(Float)
    customerid = Column(String)
    country = Column(String)
    year = Column(Integer)
    month = Column(String)
    day = Column(Integer)
    time = Column(String)
    weekday = Column(String)
    revenue = Column(Float)
    

   

if __name__ == "__main__":
    t = time()

    #Create the database
    engine = create_engine('sqlite:///csv_test10.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    
    s = session()
    try:
                    
        with open('fin_df.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
            
            dr = csv.DictReader(fin)
            
            # comma is default delimiter
            to_db = [(i['ï»¿InvoiceNo'],i['StockCode'],i['Description'],i['Quantity'],i['InvoiceDate'],i['UnitPrice'],i['CustomerID'], i['Country'],i['year'],i['month'],i['day'],i['time'],i['weekday'],i['Sales']) for i in dr]
            
        for i in to_db:
            record = Price_History(invoiceno = i[0],stockcode = i[1],description = i[2],quantity = i[3],invoicedate = i[4], unitprice = i[5], customerid = i[6],country = i[7],year = i[8],month = i[9],day = i[10],time = i[11],weekday = i[12], revenue = i[13])            
            s.add(record)
        s.commit()
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection
    print ("Time elapsed: " + str(time() - t) + " s.")
    


        

    



