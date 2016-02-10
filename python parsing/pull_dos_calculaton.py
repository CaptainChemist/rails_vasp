#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import argparse
import sys
import re
import numpy as np
import os

#Syntax is python pull_dos_calculation n, where n is the calculation number that you want to parse and enter into
#the database
parser = argparse.ArgumentParser(description='Gets info from database')
parser.add_argument('c', type=int, nargs=1)
args = parser.parse_args()

#Create path to the right calculation, Medea Materials Design will output the data into standard folders based on 
#the calculation number, so we have to set the right calcPath variable
calcName = int(args.c[0])
folderName = str(args.c)
folderName = folderName[1:-1]

if int(folderName) >= 1000:
    calcPath='/opt/MD/2.0/Jobs/dir1000/'
elif int(folderName) < 500:
    calcPath='/opt/MD/2.0/Jobs/dir500/'
calcPath=calcPath+folderName

con = None
runSQL = True

try:
    #connect to the local database
    con = psycopg2.connect(database='rails_vasp_development', user='medea')
    cur = con.cursor()
    
    #First let's check to see if that number has already been called to the database
    cur.execute(str("select id from names where calc_num = %s" % (folderName)))
    tempName =str(cur.fetchall())[2:-3]
    print(tempName)

    cur.execute(str("select * from states where name_id = %s" % (tempName)))
    name_id=cur.fetchall()
    
    #If the search compes back empty, then it skips this checking stuff
    if name_id != []:
        check = raw_input('This calc number has been previously submitted. Overwrite? yes/no \n')
        #If the user says no, then don't run the submit portion of the cod
        if check == 'n' or check =='no':
            runSQL = False
        
        #If they want to overwrite it, first search for the key column that corresponds to the calcnum
        else:
            #Now loop through the keys and delete each entry
            cur.execute("DELETE from states WHERE name_id = %s" % tempName)
            con.commit()

    
    if runSQL == True:
        #first pull the list of orbitals desired for each cluster of atoms
        cur.execute("SELECT orbital_list FROM names WHERE calc_num = %s" % calcName)
        orbitals=cur.fetchall()
        
        #next pull the list of clusters from the database
        cur.execute("SELECT cluster_list FROM names WHERE calc_num = %s" % calcName)
        cluster=cur.fetchall()
        
        #finally pull the whole list of atoms  The list should = sum(orbitals)
        cur.execute("SELECT atom_list FROM names WHERE calc_num = %s" % calcName)
        rows = cur.fetchall()

        for row in rows:
            #make a sanity check first to make sure that there are enough atoms and clusters
            if np.size(np.array(row)) != np.sum(np.array(cluster).astype(int)):
                print 'Atom count and cluster count are not equal!'
            
            #make sure the orbital and cluster list matches in size
            elif np.size(np.array(cluster).astype(int)) != np.size(np.array(orbitals)):
                print 'cluster count and orbital breakdown do not match!'

        #if everything checks out okay, then proceed
        else:
            #print np.array(cluster)[0][0].shape[0]
            cluster = np.array(cluster).astype(int).reshape((np.array(cluster)[0][0].shape[0]))
            lowestnum = 0
            for x in range(0,cluster.size):
                pathDOS = calcPath + '/DOS\ DOSCAR'
                sortPath = './_sort_dos.py'
                orbitalTest = np.array(orbitals).astype(int).reshape((np.array(orbitals)[0][0].shape[0]))[x]
                #print orbitalTest
                if orbitalTest == 2:
                    orbitalList = '0 1 2'
                elif orbitalTest == 1:
                    orbitalList = '0 1'
                elif orbitalTest == 0:
                    orbitalList = '0'
                else: orbitallist = '4'
                
                highestnum = cluster[x] + lowestnum
                atomSublist =np.array(row)[0,lowestnum:highestnum]
                lowestnum = highestnum
                os.system('python %s %s -a %s -o %s -s %s' % (sortPath, pathDOS,str(atomSublist).translate(None, ",[]()'"),orbitalList,cluster[x]))

        print 'Calculations Inserted Properly'

#This is error handling in case the database cannot connect
except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:
    
    if con:
        con.close()
