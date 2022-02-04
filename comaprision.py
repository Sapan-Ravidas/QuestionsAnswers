from itertools import count
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python comaprision.py <first_file> <second-file>")
    
    print(f"Comparision between {sys.argv[1]}, {sys.argv[2]}")
    counter = 0
    with open(sys.argv[1]) as file1:
        with open(sys.argv[2]) as file2:
            line1 = file1.readlines()
            line2 = file2.readlines()
            
    
    for l1, l2 in zip(line1, line2):
        if l1 != l2:
            counter += 1
    
    print(counter)
    