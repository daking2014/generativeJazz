import numpy as np
import leadsheet

def main():
    c, m = leadsheet.parse_leadsheet(".\\ii-V-I_leadsheets\\0001.ls")
    print(c, m)

if __name__ == '__main__':
    main()