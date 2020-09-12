def main():
    file = open('./ci_tools/pylint/file.txt', 'r')
    read = file.read()
    score = read.split()[-1]

    if score == '10.00/10':
        print('Pylint test succeeded')
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    main()