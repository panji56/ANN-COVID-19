#read library
library(lmtest)
library(regclass)

#loading data
data_covid_IHSG=read.csv(file = "../ALL_FINAL.csv")

#cleaning data
# head(data_covid_IHSG)

print("<br>")

#formula and regression
linearmodel<-lm(Close~.-Date,data = data_covid_IHSG)

#result
summary(linearmodel)

print("<br>")

RMSE=sqrt(mean(residuals.lm(linearmodel)^2))
print(RMSE)

print("<br>")

#assumption check
bptest(linearmodel)

print("<br>")

shapiro.test(residuals.lm(linearmodel))

# dwtest(linearmodel)

#correlated variables
VIF(linearmodel)