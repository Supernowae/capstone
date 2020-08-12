Note: This project is still in progress

# Capstone Project
Capstone project ATP betting

# Betting

# Inital data

# elo-score

# Tax

# EDA

# Feature engineering

# Prediction with XGBoost

## 

## Split the data
The data is split to a train set, an eval set and a test set. The reference point is the start date of testing. A few hundred samples before a used as eval set and several thousend samples befor the eval set is used as train set. A few hundred after this point are used for testing.

The different models are trained with slightly different train and eval sets. For that there is a variation of the lenght of the eval set (the differences are in the range +/- 70)

## Loss function / scorer
On the one hand we want to predict the right outcome. Especially we want to decrease the amount of *false positive* predictions so the *error* (1-accuracy) could be an appropriate scorer to minimize. (Until now in test runs the eval error was above 0.3 that means that right predictions were below 70%. Afterwarts calculated ROI was negative...)

On the other hand we want to maximize the ROI / gain. So I implemented a scorer that calculates the absolute gain of the predictions according to the odds. Due to the fact that we use a gradient **decent** method the has to be flipped to negative, because XGB wants to minimize the score. The problem is that there is no chace to pass the odds to the function. It is not possible to extract the odds as feature from the passed DMatrix. For each run the scorer function has to be created new according to the train/eval/test set with the odds as constant values in it. In the scorer a kind of thershold also can be set as hyperparameter. 

Due to the fact that each match has two samples both outcomes are treated as unique matches. I observed in test runs that sometimes the prediction for both outcomes is high (above 0,5). For that they are compared and lower one is set to 0 and the higher one passed as it is.

## Voting systems
Due to the fact that the XGB models are so instable and different in their results a voting system is required and also a strategy how to compute the confidence.
Several systems are implemented.
### Confidence
How to make the confidence for the decision? There are a some different attempts to built a confidence.
- Straight probability. Just take the probabilities of the predictors `conf=proba`.
- Confidence by the odds. Division of the probabilities by the odds  `conf=proba/odd`. It's a kind of confirmation of the opinion. If the odd is low (towards 1) and the proba high the confidence will rise. If the odd rises (lower confidence of the bookmaker / other betters) the confidence decreases.
- Log_odd confidence. The idea is to punish the probas by the odds so that the predictors have to be very sure to make a decision. `conf=log10(odd)*(10**(proba))` Assuming that if there are higher odds the probas won't be as high. It also avoids that the majority of decisions won't bet on matches with low odds where also the gain is low and the chance/risk balance isn't very good.

### Voting
For the common opinion/decision according to the above mentioned confidences of the models here are:
- The mean of the confidences of the models. Then check if the mean if above the threshold.
- Majority voting. Count how many modles confidence is above the threshold. The amount of confident models is also a hyperparameter. Due to this the amount of models is not even.

Note: The different confidence starategies may need different thresholds.

### Prediction and results

# Future work
There are several points that can be improved for better results:

- calculate surface dependent elo-scores
- maybe imrove the fuction for the elo-score
- parallelize the calculation of the features for accelerated computation and playing with the hyperparameters in the features.
- Try XGBmodels without odds in the features. The feature importance of the odds seems to be quite high so they have a large influence on the decisions. But the odds gives back the opinion / confidence of the bookmaker and other betters. I think it would be better to make an own opinion without the influence of the odds. Or maybe at least a combination of it in an ensemble that some models calculte with odds and others without and then check the voting.
- Find a way to handle the missing values un the generated features for usage with other predictors that do not accept NaNs. Then try ANN, Random Forests e.g. maybe with other boosters.
- Improve the precision. Check if the gain as loss function is the expediant way.
- Work / optimization of confidence calculation.
- Improve the voting system
- Filtering *samples* of best players and best tournament right before the model training and not only the *one-hot features*.
