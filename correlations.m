function correlations(datasetFilename)
% CORRELATIONS(datasetFilename) Print correlation coefficients between
% individual features and ratings from dataset.

    dataset = load(datasetFilename);
    dataset = dataset.dataset;
    
    features = dataset(:, 1:end-1);
    ratings = dataset(:, end);

    for i=1:size(features, 2)
        
        feature = features(:, i);
        
        R = corrcoef(feature, ratings); % Pearson's r
        fprintf('\nFeature %d\n', i);
        disp(R);
        
        % cross-correlation
        % https://www.mathworks.com/help/matlab/ref/xcorr.html
        % [c, lags] = xcorr(feature, ratings);
        % stem(lags, c)
        
    end
    
end
