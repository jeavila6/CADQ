function fig = plotAnnotation(annotation)
% PLOTANNOTATION Plot annotation and return figure.

    figWidth = 1920;
    figHeight = 1080;
    fig = figure('visible', 'off', 'position', [0,0,figWidth,figHeight]);

    X = milliseconds(1:length(annotation.ratings)) * annotation.frameSize;
    plot(X, annotation.ratings, 'linewidth', 1.5)
    
    hold on
    
    title(annotation.name, 'interpreter', 'none') % display text as typed
    xlabel('Time (mm:ss)')
    xtickformat('mm:ss')
    ylabel('Rating')
    ylim([0 20])
    grid on
    
end