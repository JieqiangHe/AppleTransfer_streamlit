import sys
import streamlit as st

header = st.container()

def get_data(filename):
    apple2what_dict_file = open(filename, 'r')
    apple2what_dict = {}
    for g in apple2what_dict_file.readlines():
        line = g.strip()
        linelist = g.split('\t')
        apple2what_dict[str(linelist[0])] = (str(linelist[1]),str(linelist[2]))
    return apple2what_dict

with header:
    st.write("""
    # 🍎 APPLE Translator
    ###### *Description: transfer Apple transcript (gene) id to TAIR id with function description.*
    """)
    species = st.multiselect("Select One Specie:", ["Arabidopsis", "Tomato"],default=["Arabidopsis"])
    if species == []:
        st.error("Please select one specie. You didn't select any specie.")
    elif species[0] == "Arabidopsis":
        apple2what_dict = get_data('data/apple2tair_v1_20220512.txt')
    elif species[0] == "Tomato":
        apple2what_dict = get_data('data/apple2itag4.txt')
    elif species == ["Arabidopsis", "Tomato"]:
        apple2what_dict = get_data('data/apple2tair_v1_20220512.txt')
        st.warning("You selected two specie. We will use Arabidopsis as default.")
    else:
        apple2what_dict = get_data('data/apple2tair_v1_20220512.txt')
    applegenes = st.text_area("🔬 Put Your Gene Matrix", help="Enter your apple gene(s) here, one gene per line.", height=200, placeholder="Enter your apple gene(s) here, one gene per line.", )
    # create result dictionary
    result = {}
    applegenes_list = applegenes.split('\n')
    linenum = 1
    for line in applegenes_list:
        g = line.strip().split('\t')[0]
        if g in apple2what_dict:
            result[linenum] = (line.strip(), apple2what_dict[g])
            linenum += 1
        else:
            result[linenum] = (line.strip(), ("NA", "NA\n"))
            linenum += 1
    list = []
    tempfile = open("temp.txt", "w")
    for k,v in result.items():
        k = str(k)
        gps = []
        gps.append(k)
        llist = v[0].split('\t')
        if len(llist) >= 1:
            for i in range(len(llist)):
                gps.append(str(llist[i]))
        gps.append(str(v[1][0]))
        gps.append(str(v[1][1]))
        list.append(gps)
        tempfile.write('\t'.join(gps))
    tempfile.close()
    st.dataframe(list)
    savename = st.text_input("Save as:", value="apple2tair_result.txt", key="savename") 
    st.success("Your result is saved as " + savename + ".")

col1, col2, col3 = st.columns(3)
col2.download_button("Download Result (.txt) 📂",data = open("temp.txt", "rb"),file_name=savename,mime="text/plain")
col2.balloons()
