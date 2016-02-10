#!/usr/bin/python

import linecache
import re
import numpy as np
import argparse
import sys
import psycopg2

parser = argparse.ArgumentParser(description='Takes processed DOS from DOSCAR and outputs summed dos for clusters of atoms.')
parser.add_argument('filename', type=argparse.FileType('r'), help='filename')
parser.add_argument('-a', nargs="+", type=int)
parser.add_argument('-o', nargs="+", type=int)
parser.add_argument('-s', nargs="+", type=int)
args = parser.parse_args()

atomNumbers = args.a
orbitalNum = args.o
howToSum = args.s
rawData=np.array(args.filename.readlines())

calcName = re.findall('\d+',str(args.filename)[0:-10])[-1]
if int(calcName) >=1000:
    calcPath='/opt/MD/2.0/Jobs/dir1000/'
elif int(calcName) < 1000:
    calcPath='/opt/MD/2.0/Jobs/dir500/'
calcPath=calcPath+calcName

#Sum clusters for DOSCAR stuff
def sumCluster(aggArray,atomNumbers,orbitalNum):
    #This saves the list of energies
	finArray = aggArray[:,0]
	First = True
	for atom in atomNumbers:
		if First:
			for orbitalType in orbitalNum:
				for x in range(1,len(aggArray[0])):
					if aggArray[0,x] == atom:
						if aggArray[1,x] == orbitalType:
							finArray = np.vstack((finArray,aggArray[:,x]))
			First = False
		else:
			count = 1
			for orbitalType in orbitalNum:
				for x in range(1,len(aggArray[0])):
					if aggArray[0,x] == atom:
						if aggArray[1,x] == orbitalType:
							finArray[count] = finArray[count]+aggArray[:,x]
							count = count + 1
	return finArray
################################################################################################
#This is the size of the histogram bin
bin = 0.05

#Splits a string into floats for initial PROCAR file reading
def getNums( string ):
	numberedList =[]
	for t in string.split():
		try:
			numberedList.append(float(t))
		except ValueError:
			pass
	return numberedList


#This handles getting and parsing of the PROCAR
def getProcar(calcPath, bin, orbital, atomSublist):
    #First select the right file
    calcLocation = calcPath + '/DOS PROCAR'
    #Open the file and save it to raw data
    f = open (calcLocation)
    rawData = np.array(f.readlines())
    
    #The keyword it is looking for is energy
    keyword = 'energy'
    binSize = bin
    First = True
    num=0
    
    #This program zeros on a particular orbital type in the procar.
    if orbital == 0 :
        Corrorbital = -4
    elif orbital == 1:
        Corrorbital = -3
    elif orbital == 2:
        Corrorbital = -2
    else: Corrorbital = 1
    
    for row in rawData:
        if num == 1:
            numAtoms=map(int, re.findall(r'\d+', row))[2]
        
        if keyword in row:
            label = getNums(row)
            label[0] = int(label[0]) #change kpoint to int
            label[2] = int(label[2]) #change orbital occupation to int
            totalDOS = getNums(row)
            totalDOS[0] = int(label[0]) #change kpoint to int
            totalDOS[2] = int(label[2]) #change orbital occupation to int
            
            for x in range(3,3+numAtoms):
                selectedLine = rawData[num+x]
                label.append(getNums(selectedLine)[Corrorbital]) #get requested dos for each atom
                totalDOS.append(getNums(selectedLine)[-1]) #get requested dos for each atom
            
            
            if First:
                procArray = np.array(label)
                procDOS = np.array(totalDOS)
                First = False
            else:
                procArray = np.vstack((procArray,label))
                procDOS = np.vstack((procDOS,totalDOS))
        num +=1
    #savename='/home/medea/medea_sql/bla'+'_raw'
    #np.savetxt(savename,procArray, fmt='%10f',delimiter=',')
    
    procArray=np.delete(procArray,0,1) #delete kpoints identifier
    procArray=procArray[procArray[:,0].argsort()] #sort by energy
    procDOS=np.delete(procDOS,0,1) #delete kpoints identifier
    procDOS=procDOS[procDOS[:,0].argsort()] #sort by energy
    
    if binSize >0:
        numIterations = 0
        First = True
        while numIterations <(numAtoms+1):
            data=procArray[:,numIterations+1]
            
            temp=np.histogram(procArray[:,0],bins=np.arange(-35,5,binSize),weights=data)[0]
            numIterations=numIterations+1
            
            maxBin = -35+binSize
            if First:
                b=np.array(np.histogram(procArray[:,0],bins=np.arange(maxBin,5,binSize),weights=data)[1])
                b=np.column_stack((b,temp))
                First = False
            else:
                b=np.column_stack((b,temp))
        procArray=[]
        procArray=b
    
    if binSize >0:
        numIterations = 0
        First = True
        while numIterations <(numAtoms+1):
            data=procDOS[:,numIterations+1]
            
            temp=np.histogram(procDOS[:,0],bins=np.arange(-35,5,binSize),weights=data)[0]
            numIterations=numIterations+1
            
            maxBin = -35+binSize
            if First:
                b=np.array(np.histogram(procDOS[:,0],bins=np.arange(maxBin,5,binSize),weights=data)[1])
                b=np.column_stack((b,temp))
                First = False
            else:
                b=np.column_stack((b,temp))
        procDOS=[]
        procDOS=b
    
    #Now I have an array that is pdos for an orbital type (energy,total occupancy, atom1, atom2...etc)
    #Add 2 to each atom s
    toAdd=np.zeros(len(atomSublist))
    toAdd.fill(2)
    toAdd=toAdd+atomSublist
    
    proC= np.sum(procArray[:,atomSublist], axis=1)
    
    proCr = (np.divide(proC,np.sum(procDOS[:,2:],axis=1))).T*(procArray[:,1])
    whereAreNaNs = np.isnan(proCr);
    proCr[whereAreNaNs] = 0;
    finArray = np.vstack([procArray[:,0],proCr])
    np.savetxt('/home/medea/medea_sql/bla_proE',procArray[:,1], fmt='%10f',delimiter=',')
    np.savetxt('/home/medea/medea_sql/bla_proA',np.sum(procArray[:,2:],axis=1), fmt='%10f',delimiter=',')
    np.savetxt('/home/medea/medea_sql/bla_proB',proC, fmt='%10f',delimiter=',')
    np.savetxt('/home/medea/medea_sql/bla_proC',np.divide(proC,np.sum(procArray[:,2:],axis=1)), fmt='%10f',delimiter=',')
    np.savetxt('/home/medea/medea_sql/bla_proCr',proCr, fmt='%10f',delimiter=',')
    
    
    return finArray



################################################################################################
#First create the list of energies for the DOS calculations:
First = True
listEnergies=[-300,-300]
numEnergies = 1
atomNum =1

trackRow = -1
for row in rawData:
	trackRow = trackRow + 1
	if First:
		for x in range (6,307):
			listEnergies.append(float(rawData[x].split()[0]))
		aggArray = np.transpose([listEnergies]) #create array for storing all the DOS data
		First = False
    #print(len(aggArray))
    
	elif len(row.split()) == 4:
		#print(aggArray)
		if str(listEnergies[2]) in row:
			currentAtom = [[atomNum,atomNum,atomNum],[0,1,2]]
			atomNum = atomNum+1
			#currentAtom = [float(rawData[trackRow].split()[1]),float(rawData[trackRow].split()[2]),float(rawData[trackRow].split()[3])]
			#print(row.split())
			for x in range(0,301):
				currentAtom = np.vstack((currentAtom,[float(rawData[trackRow+x].split()[1]),float(rawData[trackRow+x].split()[2]),float(rawData[trackRow+x].split()[3])]))
			
			aggArray = np.hstack((aggArray,currentAtom))
#print(currentAtom.shape)

aggArray[0,0]=float(rawData[5].split()[-2])

#So far we have created an array with columns that represent DOS for an atom type and orbital type
#Now we need to take the atoms passed to the function and sum by orbital type
#Example ./sortDOS rawDOS -a 1 3 6 57 -b 0 1 2 3 will take atoms 1,3,6,57 and sum the s,p,d orbitals as separate columns and also return total dos as a separate column

start=0
finArray=np.transpose(aggArray[:,0].shape)
First = True
for clusters in howToSum:
	end = start + clusters
	
	if First:
		finArray= np.transpose(sumCluster(aggArray,atomNumbers[start:end],orbitalNum))
		First = False
	else:
		finArray = np.hstack((finArray,np.transpose(sumCluster(aggArray,atomNumbers[start:end],orbitalNum))))
	start = start + clusters

#Now take the finArray and start inserting things into the postgresql database
con = None
try:
    
    con = psycopg2.connect(database='rails_vasp_development', user='medea')
    cur = con.cursor()
    
    atoms =str(atomNumbers)[1:-1]
    fermi_level = finArray[0,0]
    core_level = 1 # Not in use right now, think about pulling a core atom from the OUTCAR in the future
    
    for orbital in range(1,(finArray.shape[1])):
        energy = str(finArray[2:,0].tolist())[1:-1]
        dos =str(finArray[2:,orbital].tolist())[1:-1]
        
        orbitalNum=orbital-1
        
        occupancy=np.transpose(np.array(getProcar(calcPath, bin, orbitalNum,atomNumbers)))
        energy_occ =str(occupancy[:,0].tolist())[1:-1]
        elec_occ =str(occupancy[:,1].tolist())[1:-1]
        
        
        #insert the dos data
        cur.execute(str("select id from names where calc_num = %s" % (calcName)))
        name_id=str(cur.fetchall())[2:-3]
        cur.execute(str("INSERT INTO states (atom_subset,orbital_subset,fermi_level,core_level,energy_list, dos_list,elec_energy_list,elec_occ_list,name_id) VALUES('{%s}',%s,%s,%s,'{%s}','{%s}','{%s}','{%s}',%s)" % (atoms,orbitalNum,fermi_level,core_level,energy,dos,energy_occ,elec_occ,name_id)))
        con.commit()

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e
    sys.exit(1)


finally:
    
    if con:
        con.close()



