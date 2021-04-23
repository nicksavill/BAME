# Analysis of course marks and Honours Project marks

library(Matrix)
library(tidyr)
library(nlme)
library(ggplot2)
library(tidyverse)
library(broom)
library(car)

a <- read.table("~/QA/BAME/course_marks.csv", header=TRUE, sep=",")
a <- a %>% drop_na()

# As course marks are constrained in the interval 0 - 100
# they are arcsine-sqrt transformed to make the residuals more normal
# This transform makes negligible difference mainly because most
# marks are not at the extremes
a$lMark = asin(sqrt(a$Mark / 100))
hist(a$lMark)

aggregate(Mark ~ Fee_status+ethnicity, a, mean)

### 4th year course marks of EU students ###############################
# Have to do EU separately as there are no EU Asian students
# which mucks up the analysis if done together with other statuses
# Fortunately there is no effect of ethnicity for EU students
# This does not include final year Honours project mark
mask1 = a$Fee_status == "EU"
mask2 = a$Project == "False"  
mask3 = a$Year == 4

b <- a[mask1 & mask2 & mask3, ]
b <- droplevels(b)

# Check data look ok
some(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))

# Compare two models (maximum likelihood for model comparison by anova)
#   1) no effect of ethnicity
#   2) ethnicity as a factor
model.1a <- lme(lMark ~ 1, random=~1|ID, b, method="ML")
model.1b <- lme(lMark ~ Ethnicity, random=~1|ID, b, method="ML")
# model 1b does not improve on model 1a
# therefore no effect of ethnicity in EU students
anova(model.1a, model.1b)
Anova(model.1b, type = 2)

# Checks
r <- residuals(model.1a)
hist(r)
mean(r)
plot(model.1a)
qqPlot(r)



### 4th year course marks of non-EU students ###############################
mask1 = a$Fee_status != "EU"
mask2 = a$Project == "False"  
mask3 = a$Year == 4

b <- a[mask1 & mask2 & mask3, ]
b <- droplevels(b)

# Check data look ok
some(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))
b <- within(b, ethnicity <- relevel(ethnicity, ref = "White"))
# Make RestUK+RoI the reference level
b <- within(b, Fee_status <- relevel(Fee_status, ref = "RestUK+RoI"))
# Use helmert contrasts for fee status as we don't want to compare
# to one in particular, and this helps interpret the model's coefficients
contrasts(b$Fee_status) <- contr.helmert(3)

# Full model with interactions 
model.2a <- lme(lMark ~ Fee_status*Ethnicity, random=~1|ID, b, method="REML")

# Significant interaction between fee status and ethnicity exists
Anova(model.2a, type = 2)
summary(model.2a)

# Fit model to Mark data rather than transformed to get coefficients for report
model.2b <- lme(Mark ~ Fee_status*Ethnicity, random=~1|ID, b, method="REML")
summary(model.2b)

# Checks
r <- residuals(model.2a)
hist(r)
mean(r)
plot(model.2a)
qqPlot(r)
vif(model.2a)



### Honours Project marks of EU students ###############################
mask1 = a$Fee_status == "EU"
mask2 = a$Project == "True"

b <- a[mask1 & mask2, ]
b <- droplevels(b)

# Check data look ok
head(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))

# Full model with interactions 
model.3a <- lm(lMark ~ 1, b)
model.3b <- lm(lMark ~ Ethnicity, b)
# model 3b does not improve on model 3a
# therefore no effect of ethnicity in EU students
Anova(model.3b)
anova(model.3a, model.3b)

# Checks
r <- residuals(model.3a)
hist(r)
mean(r)
plot(model.3a)



### Honours Project marks of Non-EU students ###############################
mask1 = a$Fee_status != "EU"
mask2 = a$Project == "True"

b <- a[mask1 & mask2, ]
b <- droplevels(b)

# Check data look ok
some(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))
# Make RestUK+RoI the reference level
b <- within(b, Fee_status <- relevel(Fee_status, ref = "RestUK+RoI"))
# Use helmert contrasts for fee status as we don't want to compare
# to one in particular, and this helps interpret the model's coefficients
contrasts(b$Fee_status) <- contr.helmert(3)

# Full model with interactions 
model.4a <- lm(lMark ~ Fee_status+Ethnicity, b)
model.4b <- lm(lMark ~ Fee_status*Ethnicity, b)
Anova(model.4b, type = 2)
# No significant interaction between fee status and ethnicity
summary(model.4a)

# Fit model to Mark data rather than transformed to get coefficients for report
model.4c <- lm(Mark ~ Fee_status+Ethnicity, b)
summary(model.4c)

# Checks
r <- residuals(model.4a)
hist(r)
mean(r)
plot(model.4a)
vif(model.4a)


### 1st year course marks of EU students ###############################
mask1 = a$Fee_status == "EU"
mask3 = a$Year == 1

b <- a[mask1 & mask3, ]
b <- droplevels(b)

# Check data look ok
some(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))

# Full model with interactions 
model.5a <- lme(lMark ~ 1, random=~1|ID, b, method="ML")
model.5b <- lme(lMark ~ Ethnicity, random=~1|ID, b, method="ML")
anova(model.5a, model.5b)
# No significant effect of ethnicity
Anova(model.5b, type = 2)
summary(model.5a)

# Checks
r <- residuals(model.5a)
hist(r)
mean(r)
plot(model.5a)
qqPlot(r)



### 1st year course marks of non-EU students ###############################
mask1 = a$Fee_status != "EU"
mask3 = a$Year == 1

b <- a[mask1 & mask3, ]
b <- droplevels(b)

# Check data look ok
some(b)
levels(b$Fee_status)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))
# Make RestUK+RoI the reference level
b <- within(b, Fee_status <- relevel(Fee_status, ref = "RestUK+RoI"))
# Use treatment contrasts for fee status so we can compare fee status
contrasts(b$Fee_status) <- contr.treatment(3)

# Full model without interactions 
model.6a <- lme(lMark ~ Fee_status, random=~1|ID, b, method="ML")
model.6b <- lme(lMark ~ Fee_status+Ethnicity, random=~1|ID, b, method="ML")
anova(model.6a, model.6b)
# Fee status is the only significant effect
Anova(model.6b, type = 2)
summary(model.6a)

# Fit model to Mark data rather than transformed to get coefficients for report
model3 <- lme(Mark ~ Fee_status, random=~1|ID, b, method="REML")
summary(model3)

# Checks
r <- residuals(model.6a)
hist(r)
mean(r)
plot(model.6a)
qqPlot(r)



