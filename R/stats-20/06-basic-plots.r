load(url("http://www.stat.berkeley.edu/~nolan/data/KaiserBabies.rda"))
infants
head(infants)
#compute BMI
bmi = (infants$wt *703) / (infants$ht ^ 2) 
bmi
summary(bmi)
infants$bmi = (infants$wt *703) / (infants$ht ^ 2) 
infants
infants[1]
head(infants)
density(infants$bmi, na.rm=1)
plot(density(infants$bmi, na.rm=1))
plot(density(infants$bmi, na.rm=TRUE))
# Unimodal distribution, skewed, long tail
qs = seq(0.01, 0.99, by = 0.01)
qs
# seq in R like (x)range(0.01, 0.99, 0.01)
plot(density(quantile(infants$bmi, qs, na.rm=TRUE)))
factor(infants$smoke)
levels(infants$smoke)
bmiSmoke = subset(infants$bmi, infants$smoke == "Now" | infants$smoke == "Until Pregnant")
bmiNever = subset(infants$bmi, infants$smoke == "Never" | infants$smoke == "Once, Not Now")
plot(density(bmiSmoke, na.rm=TRUE))
plot(density(bmiSmoke, na.rm=TRUE), col = "blue")
lines(density(bmiNever, na.rm=TRUE), col = "green")
abline(v = 30, col = "grey60")
legend("topright", legend = c("None smoker", "Smoker"), fill = c("green", "blue"))
#text(30, 0.07, "Obese")
#savehistory("/home/greg/programming/R/stats-20/06-basic-plots.r")
