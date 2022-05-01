from bs4 import BeautifulSoup
import requests



#----------------------------------------------------------------
#Euro Extraction

url_euro= 'https://si3.bcentral.cl/indicadoressiete/secure/Serie.aspx?gcode=PRE_EUR&param=cgBnAE8AOQBlAGcAIwBiAFUALQBsAEcAYgBOAEkASQBCAEcAegBFAFkAeABkADgASAA2AG8AdgB2AFMAUgBYADIAQwBzAEEARQBMAG8ASgBWADQATABrAGQAZAB1ADIAeQBBAFAAZwBhADIAbABWAHcAXwBXAGgATAAkAFIAVAB1AEIAbAB3AFoAdQBRAFgAZwA5AHgAdgAwACQATwBZADcAMwAuAGIARwBFAFIASwAuAHQA'
euroResults= requests.get(url_euro)
sopa= BeautifulSoup(euroResults.text,'lxml')



table1= sopa.find_all("th")
table2= sopa.find_all("span", attrs={"class": "obs"})
#print(table2)

euro = []

for td in table2:
    if td.text!= "": 
        euro= td.text
    print(euro)    



# ----------------------------------------------------------------
#Dolar Extraction

web_url = 'https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TIPO_CAMBIO/MN_TIPO_CAMBIO4/DOLAR_OBS_ADO'
results=requests.get(web_url)
soup= BeautifulSoup(results.text,'lxml')




table= soup.find("table", attrs={"id": "grilla"})
table_data=table.tbody.find_all("tr") # 1row
table_meses= table.thead.find_all("tr")

meses= []
for th in table_meses[0].find_all("th"):
    meses.append(th.text.replace('\n', ' ').strip())




dolar= []
for td in table_data[0].find_all("td"):
    dolar.append(td.text.replace('\n', ' ').strip())


with open('exportData.txt', 'w' ) as file:
    meses.pop(0)
    dolar.pop(0)
    dolar[0]="   Dólar"
    meses[0]="\t Fecha"
    for mes,dolares in zip(meses,dolar):
        file.write(" ".join(mes) + "\t\t" + " ".join(dolares) + "\n")
