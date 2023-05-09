from Classes.StructureChart import StructureChart


def main():
    my_struc_chart = StructureChart("python_stubs_test_file.py")
    img = my_struc_chart.draw()
    img.show()

if __name__ == "__main__":
    main()