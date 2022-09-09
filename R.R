#install.packages("languageserver")
#install.packages("ggplot2",dependencies=TRUE)
#install.packages("reticulate")


#library(reticulate)
library(ggplot2)


#EuroUSD <- read.csv("C:/Users/sebas/Downloads/EuroUSD.csv", sep=",", header=TRUE, quote="\"")

#EuroUSD <- read.csv2("file:///home/giancarlo/Escritorio/proyectos/webScrapping/EuroUSD.csv", sep=",", header=TRUE, quote="\"")
EuroUSD<- read.csv2("file:///home/giancarlo/Escritorio/proyectos/webScrapping/scrapping/EURUSD.csv", sep=",", header=TRUE, quote="\"")


datos <-EuroUSD$Último
promedioDatos<- mean(datos)

print(promedioDatos)
str(EuroUSD)

EuroUSD$Fecha <- as.Date(EuroUSD$Fecha, format = "%d.%m.%Y")

class(EuroUSD$Fecha)

head(EuroUSD$Fecha)

str(EuroUSD)



write.csv(EuroUSD, "EURUSD2.csv")

generate.PDF<- function(data,prom){

    pdf(file="/home/giancarlo/Escritorio/proyectos/webScrapping/scrapping/myplot.pdf",
    onefile=T, 
    width=10,
    height=8)

    p<-ggplot(data, aes(x=Fecha, y=Último)) + 
          geom_point() +
          geom_hline(yintercept=prom, colour="red") +
          theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


    print(p)
    #X11()
    #plot(p)     
    #Sys.sleep(99999)
    #dev.off()
    ggsave("imag.jpg", plot = p) 

}

generate.PDF(EuroUSD,promedioDatos)

#m<-MASS::rlm( datos ~ Fecha, data=EuroUSD, family=binomial )

#-----. . . . . . . . . . . . . . new data extraction  ...................

#install.packages("readxl")
library("readxl")



predict<- read_excel("euro_predict.xlsx")

summary(predict)


datosPredOriginal <-predict$Reales
datosPred <-predict$Datos





reg_lin <- lm(datosPredOriginal ~ datosPred)
print(reg_lin)