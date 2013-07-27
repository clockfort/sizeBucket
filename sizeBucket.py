#!/usr/bin/python
import os
import argparse

def topBucket(numBuckets):
	for first in buckets(numBuckets):
		return first[0][0]

def buckets(numBuckets):
	yield sorted(bucketFactory(numBuckets), key=lambda x:x[1])

def bucketFactory(numBuckets):
	for num in range(numBuckets):
		bucket = "bucket" + str(num)
		yield (bucket, safeSize(bucket))

def recursiveFiles(directory):
	for root, dirnames, filenames in os.walk(directory):
		for name in (filenames + dirnames):
			yield os.path.join(root, name)

def directorySize(directory):
	size=0
	for name in recursiveFiles(directory):
		size+= safeSize(name)
	return size

def files(directory, numBuckets):
	for name in os.listdir(directory):
		bucketize(directory, name, numBuckets);

def bucketize(directory, filename, numBuckets):
	os.symlink( os.path.join(directory, filename), os.path.join(topBucket(numBuckets), filename))

def safeSize(name):
	if os.path.exists(name):
		if os.path.isdir(name):
			return directorySize(name)
		else:
			return os.path.getsize(name)
	else:
		os.mkdir(name)
		return directorySize(name)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='sizeBucket')
	parser.add_argument('-n', '--numBuckets', type=int, default=8, help='number of buckets to create')
	parser.add_argument('directory', type=str, default='.', help='directory to subdivide')
	args = parser.parse_args()
	files(os.path.abspath(args.directory), args.numBuckets)
