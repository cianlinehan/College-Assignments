BMI.df = read.table('BMI.txt', header=T)
attach(BMI.df)
#q1
#Student ID number : **** Add 0.381 to BMI:
BMI.df[,2] = BMI.df[,2] + .381
BMI.df = BMI.df[,-8]

bmi.lm = lm(BMI.df$BMI~BMI.df$Waist)
plot(BMI.df$Waist,BMI.df$BMI,main='Plot of Waist (cm) vs BMI (kg/m2)')
abline(bmi.lm)

summary(bmi.lm)
qt(.975, 78)
0.32985 - (1.990847*0.02017)

t = (.3-0.32985/0.02017)
t
1-pt(.975,78)

predict(bmi.lm, newdata=data.frame(Waist=c(88)))

#2
bmi2.lm = lm(BMI.df$BMI~BMI.df$Waist + BMI.df$Leg + BMI.df$Elbow + BMI.df$Wrist + BMI.df$Arm)
summary(bmi2.lm)
qf(.975,5,74)

bmi3.lm = lm(BMI.df$BMI~BMI.df$Waist + BMI.df$Leg + BMI.df$Arm)
anova(bmi3.lm,bmi2.lm)

cor(BMI.df)
bmi4.lm = lm(BMI.df$BMI~BMI.df$Waist + BMI.df$Leg + BMI.df$Wrist + BMI.df$Arm)
anova(bmi4.lm, bmi2.lm)

#3
bmi.resid=resid(bmi2.lm)
bmi.resid[1]

hat = lm.influence(bmi2.lm)$hat
s = summary(bmi2.lm)$sigma
r = (bmi.resid)/(s*(1-hat)^.5)
plot(r,type='h', main='Plot of Studentized Residuals vs. observation number')
abline(h=0,lty=1)
abline(h=c(-2,2),lty=2)
identify(r, n=1)
r[62]

plot(hat, type='h',main="Plot of Leverage vs. observation number", ylab ="Leverage")
identify(hat,n=3)
hat[73]
BMI.df[73,]
summary(BMI.df$Waist)
summary(BMI.df$Leg)
summary(BMI.df$Elbow)
summary(BMI.df$Wrist)
summary(BMI.df$Arm)

p = length(coef(bmi2.lm))
d = (1/p)*(hat/(1-hat))*r^2
plot(d,type='h',  main="Plot of Cook's Distance vs. observation number", ylab="Cook's distance")
identify(d, n=2)

r[73]
r[62]
hat[73]
hat[62]

#4
par(mfrow=c(2,2))
#model 1
bmi = BMI.df$BMI
elbow = BMI.df$Elbow
scatter.smooth(elbow, bmi, main='Smooth.scatter Plot')
lm1 = lm(bmi~elbow)
plot(fitted(lm1), resid(lm1), main='Plot of Residual V Fitted Values')
abline(h=0,lty=2)
hist(resid(lm1), main='Histogram of Residuals')
qqnorm(resid(lm1),main='Normal Probability Plot of Residuals')
qqline(resid(lm1))

#model 2
bmi = BMI.df$BMI
elbow = BMI.df$Elbow
scatter.smooth(elbow, log(bmi), main='Smooth.scatter Plot')
lm1 = lm(log(bmi)~elbow)
plot(fitted(lm1), resid(lm1), main='Plot of Residual V Fitted Values')
abline(h=0,lty=2)
hist(resid(lm1), main='Histogram of Residuals')
qqnorm(resid(lm1),main='Normal Probability Plot of Residuals')
qqline(resid(lm1))

#model 3
bmi = BMI.df$BMI
elbow = BMI.df$Elbow
scatter.smooth(log(elbow), log(bmi), main='Smooth.scatter Plot')
lm1 = lm(log(bmi)~log(elbow))
plot(fitted(lm1), resid(lm1), main='Plot of Residual V Fitted Values')
abline(h=0,lty=2)
hist(resid(lm1), main='Histogram of Residuals')
qqnorm(resid(lm1),main='Normal Probability Plot of Residuals')
qqline(resid(lm1))

#5
bmi.means = read.table('BMImeans(1).txt',header=T)
#Student ID number = 119301381 Add 0.381 to BMI means:
bmi.means[,3] = bmi.means[,3] + .381

1-pchisq(105.6815, 78)
summary(bmi5.lm)
deviance(bmi5.lm)/16
qchisq(.95,78)

bmi5.lm = lm(BMI.df$BMI~BMI.df$Wrist)
bmi.weighted.lm = lm(bmi.means$BMImean~bmi.means$WristValue, weights = bmi.means$n )
anova(bmi5.lm)
anova(bmi.weighted.lm)
summary(bmi5.lm)

sslof = 384.03
dflof = 19
sspe = 1690.9 - sslof
dfpe = 78 - dflof
Fstat = (sslof/dflof)/(sspe/dfpe)
Fstat
qf(.95, dflof, dfpe)
pf(.9124964,dflof,dfpe)

individual.aov = aov(BMI.df$BMI~ factor(BMI.df$Wrist))
anova(bmi5.lm, individual.aov)

#6
options(contrasts=c(factor="contr.treatment",
                     ordered="contr.poly"))

seperate.lm = lm(BMI.df$BMI ~BMI.df$Waist + BMI.df$BP + BMI.df$Waist:BMI.df$BP)
parallel.lm = lm(BMI.df$BMI ~BMI.df$Waist + BMI.df$BP)
anova(parallel.lm,seperate.lm)
summary(seperate.lm)

same.lm = lm(BMI.df$BMI~BMI.df$Waist)
anova(same.lm, seperate.lm)
summary(parallel.lm)

