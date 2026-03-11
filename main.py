from glucose import load_cgm_data,load_insulin_data
def main():
    cgm_file="/home/laiscuckoo/Downloads/Junk/cgm.csv"
    insulin_file="/home/laiscuckoo/Downloads/Junk/insulin.csv"
    cgm = load_cgm_data(cgm_file if cgm_file else None)
    insulin = load_insulin_data(insulin_file if insulin_file else None)
    cgm = load_cgm_data(cgm_file)
    insulin = load_insulin_data(insulin_file)
    print(cgm, insulin)   
    
    print("Hello from try!")


if __name__ == "__main__":
    main()
