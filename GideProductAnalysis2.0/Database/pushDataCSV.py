'''
#################################################
@product: Gide Product Analysis
@filename: Database Construction

@author: Michael Brock Li
@date: December 16th 2018
##################################################
'''

import psycopg2
import sys

SQL_STATEMENT = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """
    
def csv_to_table(tablevalues, filepath, tablename, dbname, host, port, userID, pwd, func):
    
    '''
    @purpose: Create new tables for database and copy CSV files information with table
    headers to the database tables. 
     
    @inputs: tablevalues [big string], filepath [string], tablename [string], dbname [string],
    host [int], port [int], userID [int], pwd = "" [string], func [string] 
    @outputs: None (database creation and update)
    '''
    
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=userID)
        
        cur = conn.cursor()
        
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (tablename,))
        filename = open(filepath, "r")
        
        if (cur.fetchone()[0]):
            if func == 'w' and tablename == 'author_table':
                cur.execute('''ALTER TABLE '''+tablename+''' 
                DROP COLUMN user_score, DROP COLUMN word_count_score, DROP COLUMN quality_word_score,
                DROP COLUMN review_sentiment_score, DROP COLUMN word_reptition_score, DROP COLUMN low_quality_score,
                DROP COLUMN verified_purchase_score, DROP COLUMN category, DROP COLUMN review_text, 
                DROP COLUMN word_repetition_percentage; ''')
            
            if func == 'w' and tablename == 'review_table':
                cur.execute('''ALTER TABLE '''+tablename+''' 
                DROP COLUMN review_sentiment_score, DROP COLUMN review_score;''')

            if func == 'w' and tablename == 'sentencelabelling':
                cur.execute("Truncate {} Cascade;".format(tablename))

            cur.copy_expert(sql = SQL_STATEMENT % tablename, file = filename)
                        
        else:
            cur.execute("CREATE TABLE "+tablename+" "+tablevalues)
            cur.execute("Truncate {} Cascade;".format(tablename))
            #print("Truncate {} Cascade;".format(tablename))
            cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(tablename), filename)
        
        #cur.execute("DELETE FROM "+tablename+ " a USING)
        cur.execute("commit;")
        print("Loaded data into {}".format(tablename))
        conn.close()
        print("DB connection closed.\n")
    
    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(4)
    