#!/usr/bin/python3

RESULTS_FILE = "results.txt"
OUTPUT = "records.html"

def main():
    data = []

    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line.count(" ") != 3:
                continue

            timestamp, text, name, speed = line.split(" ")
            timestamp = int(timestamp)
            speed = int(speed)

            data.append([timestamp, text, name, speed])

    print("== All texts ==")
    for d in sorted(data, key=lambda d: d[3], reverse=True):
        print("%-30s %10s" % (d[2], d[3]))
    
    prev = ""
    text_num = 0
    for d in sorted(data, key=lambda d: (d[1], d[3], d[0]), reverse=True):
        if d[1] != prev:
            prev = d[1]
            print()
            print("== Text %d ==" % (text_num + 1))
            text_num += 1

        print("%-30s %10s" % (d[2], d[3]))



if __name__ == "__main__":
    main()