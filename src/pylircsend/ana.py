import sys

def main():
    file = sys.argv[1]
    
    print('{0}:'.format(file), end='')

    with open(file, 'r') as f:
        s = False
        c = 0

        for l in f:
            d = l.split(' ')
            t = d[0]
            v = int(d[1])
            c = c + 1
            
            if v > 8000 and c > 10:
                s = True
                c = 0
                
            if s == True and c > 2 and t == 'pulse':
                if v > 800:
                    print('1', end='')
                else:
                    print('0', end='')

    print('')

if __name__ == '__main__':
    main()
