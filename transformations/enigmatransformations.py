def classfill(dFrame, classCol, siteCol, idxRange):
    """Fills missing values with means of a class

    Inputs
    ------
    dFrame:   Pandas dataframe to process (type: dataframe)

    classCol: String indicating dataframe column name containing class information

    siteCol:  String indicating dataframc column name containing class information

    idxRange: 2x1 vector indicating lower and upper bound of data to fill in dataframe
              idxRange[0] is lower bound
              idxRange[1] is upper bound

    Returns
    -------
    data:     Dataframe will all missing values filled
    """
    uniqClass = dFrame[classCol].unique()                   # All unique classes
    uniqSites = dFrame[siteCol].unique()                    # All unique sites
    print('...found ' + str(uniqClass.size) + ' classes across ' + str(uniqSites.size) + ' sites')
    print('...filling missing data with class means')
    data = dFrame.loc[:, idxRange[0]:idxRange[1]]           # Extract all numerical value from 'dBegin' onwards
    for site in uniqSites:
        siteIdx = dFrame.loc[:, siteCol] == site            # Index where site is uniqSite = site
        for cls in uniqClass:
            classIdx = dFrame.loc[:, classCol] == cls       # Index where class is uniqClass = cls
            idx = siteIdx & classIdx                        # Index where both class and site indexes are true
            for col in range(len(data.columns)):            # Iterate along each column
                nanIdx = data.iloc[: ,col].isnull()         # Index where NaNs occur per feature
                nanIdx_i = nanIdx & idx                     # Index where NaNs occur per feauture, per site, per class
                if np.sum(nanIdx_i) > 0:
                    mean = np.nanmean(data.iloc[:, col][idx]) # Compute mean of non-NaNs# If there are any Nans...
                    data.iloc[:, col][nanIdx_i] = mean      # Replace NaNs with mean
    dFrame.loc[:, idxRange[0]:idxRange[1]] = data           # Substitute dataframe with corrected data
    return dFrame

def minorityclass(dFrame, classCol):
    """Returns the minority class label in a set of binary class labels

    Inputs
    ------
    dFrame: Pandas Dataframe containing tabular data

    classCol: Column label containing class information (string)

    Returns
    -------
    minorClass: String depicting minor class

    disparity: Integer indicating disparity between minor and major classes
    """
    uniqClass = dFrame[classCol].unique()  # All unique classes
    nClass = np.zeros((uniqClass.shape), dtype=int)
    for i, classVal in enumerate(uniqClass):
        nClass[i] = np.sum(dFrame.loc[:, classCol] == classVal)
    minorIdx = np.argmin(nClass)
    minorClass = uniqClass[minorIdx]
    majorIdx = np.argmax(nClass)
    disparity = nClass[majorIdx] - nClass[minorIdx]
    return minorClass, disparity