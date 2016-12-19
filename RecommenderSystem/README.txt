GROUP NAME: D504E16 
This is an overview of our code. 
The folder names and their descriptions are displayed at the bottom of this README.

RUNNING THE HYBRID RECOMMENDER
To run our Hybrid Recommender, run the code "Final Solution/FinalSolution.py" with the Python 3.5.2 interpreter. 
This will print 10 recommendations for every user.

FOLDER NAME                      DESCRIPTION
-----------------------------------------------------------------------------------
Baseline                         Baseline predictor
ColdStart                        Code for calculating amount of cold start items and users
DataAnalysis                     Code for analysing the Movielens 10K dataset 
DataAPI                          Code for getting info out of FinalData
DatasetCombination               Code for converting Movielens Dataset 10K into our format* (FullData)
Evaluation                       Code for evaluation
Final Solution                   Our Hybrid Recommender
FullData                         Movielens 10K dataset in our format*
FullDataSource                   Movielens 10K dataset in native format
Matrix Factorization             Matrix Factorization without bias
Matrix Factorization V.2         Matrix Factorization with bias
Test1			         Converted Ratings for test set 1
Test2			         Converted Ratings for test set 2
Test3			         Converted Ratings for test set 3
Test4			         Converted Ratings for test set 4
Test5			         Converted Ratings for test set 5
v2.0NearestNeighbour             K-Nearest Neighbour without Baseline
v2.1NearestNeighbour             K-Nearest Neighbour with Baseline
Weighted Content Based           Content Based with improvements

*Our format is explained in a file named FORMAT in the FullData folder.