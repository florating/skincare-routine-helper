import sys

print(f"This is the name of this program: {sys.argv[0]}")
print(f"Number of elements including the name of the program: {len(sys.argv)}")
print(f"Number of elements including the name of the program: {len(sys.argv)-1}")
print(f"Argument List: \n {str(sys.argv[1:])}")

print(f"type(sys.argv[-1]) = {type(sys.argv[-1])}")