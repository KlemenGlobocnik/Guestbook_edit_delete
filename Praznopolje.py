def praznoime(ime):
    if ime=="":
        return "Neznan"
    else:
        return ime


def main():
    print praznoime("Neznan")

if __name__=="__main__":
    main()