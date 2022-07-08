import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print("Linopt was started with wrong input")
        print("Use\n\t>>> python linopt.py YOUR_CSV_FILE.csv\nor\n\t>>> python linopt.py gui\n\t(Experimental)")
        exit(1)

