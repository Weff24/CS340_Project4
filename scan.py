import sys


def main():
    if len(sys.argv) != 3:
        return
    
    output_f = sys.argv[2]

    websites = []
    with open(sys.argv[1]) as input_f:
        for line in input_f:
            websites.append(line.split("\n")[0])

    for website in websites:
        


if __name__ == "__main__":
    main()



