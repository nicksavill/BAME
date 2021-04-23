# Analysis of Percent high classifications
# EU treated separately from Overseas, RestUK and Scottish

library(tidyr)
library(tidyverse)
library(broom)
library(car)

a <- read.table("/home/njs/QA/BAME/awards.csv", header=TRUE, sep=",")
a <- a %>% drop_na()

b <- a

# Check data look ok
some(b)

# Make White the reference level
b <- within(b, Ethnicity <- relevel(Ethnicity, ref = "White"))
# Make RestUK+RoI the reference level
b <- within(b, Fee_status <- relevel(Fee_status, ref = "RestUK+RoI"))
# Use helmert contrasts for fee status as we don't want to compare
# to one in particular, and this helps interpret the model's coefficients
contrasts(b$Fee_status) <- contr.helmert(4)

# Compare two models
#   1) no interactions between fee status and ethnicity
#   2) interactions between fee status and ethnicity
model2 <- glm('high ~ Fee_status+Ethnicity', data=b, family=binomial)
model3 <- glm('high ~ Fee_status*Ethnicity', data=b, family=binomial)
# model 2 does not improve on model 1
Anova(model3, type = 2)
summary(model2)

