print ("start of script")
print(datetime.datetime.now())
start_time = datetime.datetime.now()


# Create Dataframe from our data.
aa = ["TABLEU", "C1_AGE", "C1_RANKING", "C1_HANDNESS", "C1_WEAPON", "C2_AGE",
      "C2_RANKING", "C2_HANDNESS", "C2_WEAPON", "WINNER"]

dataframe = pd.read_csv(r"6_competition_frankings_columns.csv")
dataframe = pd.read_csv(r"6_competition_frankings_columns.csv", header=1, names=aa)
dataframe = dataframe.drop(dataframe[dataframe['C2_WEAPON'] == ' None '].index)
dataframe = dataframe.drop(dataframe[dataframe['C1_WEAPON'] == ' None '].index)
dataframe.to_csv("testing_csv")


# Split data from train to test
X = np.array(dataframe.drop(['WINNER'],1))
y = np.array(dataframe['WINNER'])
x1, x2, y1, y2 = train_test_split( X, y, random_state = 100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=3)

# Initialize max variables
max_score = 0
max_k = 0
max_leaf_size = 0
max_p = 0

k_iterations = range(0, 10)
leaf_size_ranges = range(1, 60)
p_ranges = range(1, 20)

# Test different K value
for k_value in k_iterations:
    k_range = range((k_value * 25) + 1, (k_value * 25) + 26)
    scores = []
    for k in k_range:

        # Explore the value for leaf_sie
        for leaf_size_i in leaf_size_ranges:

            # Explore the value for p
            for p_value in p_ranges:
                knn = KNeighborsClassifier(n_neighbors=k,
                                           leaf_size=leaf_size_i,
                                           p=p_value,
                                           n_jobs=5)
                knn.fit(X_train, y_train)
                y_pred = knn.predict(X_test)
                score = accuracy_score(y_test, y_pred)
                if score > max_score:
                    max_score = score
                    max_k = k
                    max_leaf_size = leaf_size_i
                    max_p = p_value

        print ("End of k test:")
        print (k)

    print ("End of iteration:")
    print (k_value)
    print ("Time elapsed:")
    print (datetime.datetime.now() - start_time)


print ("max_score")
print (max_score)
print ("max_k")
print (max_k)
print ("max_leaf_size")
print (max_leaf_size)
print ("max_p")
print (max_p)

print ("end of the script")
end_time = datetime.datetime.now()
print(end_time)
print("Total time:")
print (end_time - start_time)
