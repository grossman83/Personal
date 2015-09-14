# import numpy as np
import random
import pdb

def create_hill(min, max, length):
	a = [0]
	for k in range(length):
		a.append(random.randint(min,max))
	a.append(0)
	return a

def delta(lst):
	a = lst[0:-1]
	b = lst[1:]
	return [k[1] - k[0] for k in zip(a,b)]


hill = create_hill(0, 100000, 200000)
diff = delta(hill)
# print hill
# print diff

#peaks exist where the delta is less than zero
#peaks is an array of True, False for whether or not a peak exists at every spot

# find indices where diff < 0
ispeak = map(int, [k<0 for k in diff])
# print ispeak

#make a list intersperced with zeros containing all the peaks
peakindices = [k[0]*k[1] for k in zip(ispeak, range(len(ispeak)))]
numpeaks = sum(ispeak)
numzeros = len(peakindices) - sum(ispeak)


#this worked, but was slow. I assume it's because it has to search from the 
#beginning of the list each time and must pass the whole list around everytime.
# while numzeros > 0:
# 	peakindices.remove(0)
# 	numzeros -= 1

#peakindices is now the indices of all peaks in the hill profile
peakindices = [value for value in peakindices if value != 0]
# print peakindices


# Now, for a given peak index, search for the next inded in the hillprofile
# that is equal or greater to the height of the hill where the peak occurred.
# Then subtract from the original peak height all others and sum them. if
# no further peak is reached that is higher or equal, move to next peak index
# and repeat.
peakheight = hill[peakindices[0]]
valley = []
water = []
nextindex = peakindices[0]+1
count = 0
while count < max(peakindices) -1:
	while hill[nextindex] < peakheight and nextindex < len(hill) - 1:
		valley.append(hill[nextindex])
		nextindex += 1
		# pdb.set_trace()

	
	# print 'valley:'
	# print valley
	if nextindex > max(peakindices) - 1:
		break
	water.append(sum([peakheight - k for k in valley]))
	# if nextindex < max(peakindices)-1:
	# 	water.append(sum([peakheight - k for k in valley]))
	# else:
	# 	break


	count = nextindex
	# the count may have jumped smaller peaks and we now need to bump the count
	# to start at the next peak rather than at where it reached an equally high
	# place.
	rempeaks = [k for k in peakindices if k > count-1]
	if not rempeaks:
		break
	else:
		nextindex = rempeaks[0]
		peakheight = hill[nextindex]
	valley = []
	nextindex += 1
	# pdb.set_trace()

waterTotal = sum(water)

# print 'water:'
# print water
print 'water sum: %i' %(sum(water))
