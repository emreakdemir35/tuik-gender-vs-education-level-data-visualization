import pandas as pd
import matplotlib.pyplot as plt



import chardet

with open("Education_Data.csv", "rb") as f:
    result = chardet.detect(f.read())
print(result)




'''
df = pd.DataFrame(
    {
        "Name" : ["Emre Akdemir",
                  "Alkın Türksoy",
                  "Burak Bulak",
                  "Enes Ceran"],
        "Age" : [20,20,19,20],
        "Gender" : ["Male","Male","Male","Female"],
        "Penis Size" : [17,8,5,2.5]
    }
)

#Each column in a DataFrame is called Series.
#A table of data is stored as a pandas DataFrame.


print(df)

print(df["Age"])


ages = pd.Series([42,37.5,47,34], name="Ayak Numarası")

print(ages)

print(df.describe()) #Provides a quick overview of the numerical data
'''

education_txt = open("Education_Data.csv","r",encoding="utf-8-sig")
education = pd.read_csv("Education_Data.csv",encoding="utf-8-sig")

gender_list = []
age_gap_list = []
education_level_list = []
total_number_list = []

i = 0
for line in education_txt:
    i += 1
    if i >= 6:
        line.strip()
        first_reference_index = line.find(" ")
        gender_txt = line[1:first_reference_index:]
        gender_list.append(gender_txt)
        second_reference_index = line.find(" ",first_reference_index+1)
        third_reference_index = line.find(" ", second_reference_index+1)
        fourth_reference_index = line.find(" ", third_reference_index+1)
        fifth_reference_index = line.find("|", 1)
        seventh_reference_index = line.find("|", fifth_reference_index+1)
        age_gap_txt = line[second_reference_index+1:third_reference_index]
        age_gap_list.append(age_gap_txt)
        education_level_txt = line[fourth_reference_index : line.find("|",second_reference_index)]
        education_level_list.append(education_level_txt)
        total_number_txt = line[seventh_reference_index+1:-2]
        total_number_list.append(total_number_txt)
    else:
        continue
total_number_list.pop(-1)
education_level_list.pop(-1)
age_gap_list.pop(-1)
gender_list.pop(-1)
total_number_list = list(map(float,total_number_list))

gender = pd.Series(gender_list,name="Cinsiyet")
age_gap = pd.Series(age_gap_list,name="Yaş Aralığı")
education_level = pd.Series(education_level_list,name="Eğitim Seviyesi")
total_number = pd.Series(total_number_list,name="Toplam Kişi Sayısı")



data = pd.concat([gender,age_gap,education_level,total_number],axis=1)


#print(gender)
#print(age_gap)
#print(education_level)
#print(total_number)

'''
#gender vs total_number
grouped = data.groupby("Cinsiyet")["Toplam Kişi Sayısı"].sum()

grouped.plot(kind="bar", title="Toplam Kişi Sayısı - Cinsiyete Göre Dağılım")
plt.xlabel("Cinsiyet")
plt.ylabel("Toplam Kişi Sayısı")
plt.tight_layout()
plt.show()
'''

data["Eğitim Seviyesi"] = data["Eğitim Seviyesi"].str.strip()

order = ["Bilinmeyen","Okuma Yazma Bilmeyen","Okuma Yazma Bilen Fakat Bir Okul Bitirmeyen","İlkokul","İlköğretim","Ortaokul Veya Dengi Meslek Ortaokul","Lise Ve Dengi Meslek Okulu","Yüksekokul Veya Fakülte", "Yüksek Lisans (5 Veya 6 Yıllık Fakülteler Dahil)","Doktora"]


data["Eğitim Seviyesi"] = pd.Categorical(data["Eğitim Seviyesi"], categories=order, ordered=True)


grouped = data.groupby(["Eğitim Seviyesi","Cinsiyet"])["Toplam Kişi Sayısı"].sum().unstack()

grouped.plot(kind="bar", figsize=(10,6))
plt.rcParams["font.family"] = "DejaVu Sans"
plt.title("Eğitim Seviyesine Göre Cinsiyet Dağılımı")
plt.xlabel("Eğitim Seviyesi")
plt.ylabel("Toplam Kişi Sayısı")
plt.legend(title="Cinsiyet")
plt.tight_layout()
plt.show()

print(data["Eğitim Seviyesi"].unique())
print(grouped)