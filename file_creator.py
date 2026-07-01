def write_txt(file_name,headings,data):
    with open(f"{file_name}.txt","w") as f:
        f.write(f"{headings}\n")
        for i in data:
            # print(i)
            print("\n")
            for x in i:
                a = f"{x:<30}\t"
                f.write(a)
