#!/usr/bin/env python

import random
import math

numDataPoints = 36									# User changeable parameter: the number of data points
ClusterHierarchy = [3,2,2]								# User changeable parameter: the cluster hierarchy. The first number is the
											# number of clusters at the top level, and the successive numbers are the number of
											# sub-clusters in the cluster above.
# Parameters below this are not user changeable
xmax = 0										# sets the range of x from 0 to xmax
ymax = 0										# sets the range of y from 0 to ymax
zmax = 0										# sets the range of z from 0 to zmax
levels = 0										# sets the number of levels of sub clusters to levels
numclust = []										# describes the number of clusters at each level, with 0 being the top level



def clustergenexec(numdata, numcluster, rangex, rangey, rangez, mindist, lvls):		# Generates numdata data points making up numcluster clusters with levels of sub-clusters
    global xmax
    global ymax
    global zmax
    global level
    global numclust

    xmax = rangex									# sets the maximum x-value to user input
    ymax = rangey									# sets the maximum y-value to user input
    zmax = rangez									# sets the maximum z-value to user input
    levels = lvls									# sets the number of levels of sub-clusters to user input
    numclust = numcluster								# sets the list of number of clusters at each cluster sublevel to user input

    centers = []
    data = []
    num = numclust[0]
    newmin = math.sqrt(mindist)  							# uses a formula to determine the new minimym distance between centers of clusters
    # mindist ** 2 / (2 * (rangex + rangey + rangez) / 6 )
    i = 0

    while i < num:									# a loop to create the coordinates for necessary centers using a random number generator
	x = random.random() * rangex
	y = random.random() * rangey
	z = random.random() * rangez
	if x >= 0 and y >= 0 and z >= 0 and x <= xmax and y <= ymax and z <= zmax:	# checks to see if the new center is within bounds
	    centers.append((x, y, z))
	for j in range(0, len(centers) - 1):						# checks to see if the new center is too close
	    if math.sqrt((centers[j][0] - centers[i][0])**2 + (centers[j][1] - 
	    centers[i][1])**2 + (centers[j][2] - centers[i][2])**2) < mindist:
		del centers[i]								# if center is too close, delete it from the list
		i -= 1									# go back and redo this one
	i += 1

    if levels > 0:									# if there are sublevels, call helper function for sublevels and input data
	for i in range(0, num):								# loop to generate enough clusters that will have subclusters
	    data.append(clustergen(numdata // num, mindist / 2.0, newmin,
	    levels - 1, centers[i]))							# call helper function
    elif levels == 0:									# if there are no sublevels, then generate the clusters and we're done
	numperclust = numdata // num							# determined the number of data per cluster
	for i in range(0, num):								# a loop that generates user-specified number of clusters
	    data.append(clusterfromcenter(centers[i], numperclust, mindist / 2.0))	# appends a list of data points from a designated center

    return data



def clustergen(numdata, radius, mindist, levels, center):				# Checks to see if we need more sub-clusters then calls necessary function
    global numclust
    num = numclust[len(numclust) - levels - 1]						# finds out how many clusters there will be 
    temp = []
    newmin =  math.sqrt(mindist)  							# determines the new minimum distance between centers of clusters
    # mindist**2.0 / (2.0 * radius)

    if levels == 0:									# if this is the final layer of subclustering, call helper
	return clusterhelper(numdata, num, radius, mindist, center)			# calls helper
    elif levels != 0:									# if this isn't the final layer of subclustering, call itself
	centers = centergen(num, radius, mindist, center)				# creates centers for the subclusters
	for i in range(0, num):								# loop to create enough subclusters
	    temp += clustergen(numdata // num, mindist / 2.0, newmin,
	    levels - 1, centers[i])							# add subclusters to overall list of data
	return temp



def clusterhelper(numdata, numcluster, radius, mindist, center):			# Creates final layer of sub-clusters
    centers = centergen(numcluster, radius, mindist, center)				# generates centers
    numperclust = numdata // numcluster							# determines number of data per cluster
    clusters = []

    for i in range(0, numcluster):							# loop to create enough clusters
	clusters += clusterfromcenter(centers[i], numperclust, mindist / 2)		# adds generated data to a list

    return clusters



def clusterfromcenter(center, numdata, radius):						# Generates numdata data points centered at center within radius of the center
    data = []
    global xmax
    global ymax
    global zmax
    i = 0

    while i < numdata:									# loop to generate enough data
	r = random.gauss(0, 1) * radius							# uses a gaussian distribution to determine the radius
	theta = random.random() * 2 *  math.pi						# randomly generates a theta angle in radians
	phi = random.random() * math.pi							# randomly generates a phi angle in radians
	x = r * math.sin(phi) * math.cos(theta)						# converts to get euclidean x-coord
	y = r * math.sin(phi) * math.sin(theta)						# converts to get euclidean y-coord
	z = r * math.cos(phi)								# converts to get euclidean z-coord
	if (x + center[0] <= xmax) and (y + center[1] <= ymax) and (z +
	center[2] <= zmax) and (x + center[0] >= 0) and (y + center[1] >= 0) and (z + 
	center[2] >= 0):								# checks to see if the data are within bounds
	    data.append((x + center[0], y + center[1], z + center[2]))			# adds data to the list if it's good
	    i += 1


    return data



def centergen(numcenter, radius, mindist, refpoint): 					# Generates numcenter centers within radius of refpoint
    centers = []
    i = 0

    while i < numcenter:								# loop to generate requested number of centers
	r = random.gauss(0, 1) * radius							# uses a gaussian distribution to determine the radius
	theta = random.random() * 2 *  math.pi						# randomly generates a theta angle in radians
	phi = random.random() * math.pi							# randomly generates a phi angle in radians
	x = r * math.sin(phi) * math.cos(theta)						# converts to get euclidean x-coord
	y = r * math.sin(phi) * math.sin(theta)						# converts to get euclidean y-coord
	z = r * math.cos(phi)								# converts to get euclidean z-coord
	if  (x + refpoint[0] >= 0) and (y + refpoint[1] >= 0) and (z +
	refpoint[2] >= 0) and (x + refpoint[0] <= xmax) and (y +
	refpoint[1] <= ymax) and (z + refpoint[2] <= zmax):				# checks to see if the centers are within bounds
	    centers.append((x + refpoint[0], y + refpoint[1], z + refpoint[2]))		# adds centers to list if they're good
	    for j in range(0, len(centers) - 1):					# loop to check if center is too close
		if math.sqrt((centers[j][0] - centers[i][0])**2 + (centers[j][1] -
		centers[i][1])**2 + (centers[j][2] - centers[i][2])**2) < mindist:	# checks if center is too close
		    del centers[i]							# deletes center if it's too close
		    i -= 1								# do it again
	    i += 1

    return centers

# xmax = 10
# ymax = 10
# zmax = 10
# print centergen(2, 5, 1, (0,0,0))
# print clusterfromcenter((1,1,1), 4, 5)
# print clustergenexec(12, [3,2], 1000, 1000, 1000, 10, 1)
l = clustergenexec(numDataPoints, ClusterHierarchy, 100000, 100000, 100000, 20, 2)
print "Number of clusters: ", len(l)
print "Number of data points in each cluster: ", len(l[0])
print "Number of dimensions: 3"
for i in range(0,len(l)):
    for j in range(0,len(l[i])):
	print l[i][j]
# print "data: ", l