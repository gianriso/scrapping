#install.packages("languageserver")
#install.packages("ggplot2",dependencies=TRUE)
library(ggplot2)
#EuroUSD <- read.csv("C:/Users/sebas/Downloads/EuroUSD.csv", sep=",", header=TRUE, quote="\"")

#EuroUSD <- read.csv2("file:///home/giancarlo/Escritorio/proyectos/webScrapping/EuroUSD.csv", sep=",", header=TRUE, quote="\"")
EuroUSD<- read.csv2("file:///home/giancarlo/Escritorio/proyectos/webScrapping/EURUSD.csv", sep=",", header=TRUE, quote="\"")

datos <-EuroUSD$Último
promedioDatos<- mean(datos)

print(promedioDatos)
str(EuroUSD)

EuroUSD$Fecha <- as.Date(EuroUSD$Fecha, format = "%d.%m.%Y")

class(EuroUSD$Fecha)

head(EuroUSD$Fecha)

str(EuroUSD)


p<-ggplot(EuroUSD, aes(x=Fecha, y=Último)) + 
          geom_point() +
          geom_hline(yintercept=promedioDatos, colour="red") +
          theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
X11()
plot(p)
Sys.sleep(99999)
#m<-MASS::rlm( datos ~ Fecha, data=EuroUSD, family=binomial )


