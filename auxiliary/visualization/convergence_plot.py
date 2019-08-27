import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
   
        
def convergence_plot(real_mean, sample, stat_name, n_draws, color):  
    """This function is a custom-made wrapper around
    matplotlib.pyplot.plot to depict the convergence behavior of
    the Quantities of Interest.

    Parameters
    ----------
    real_mean: float
        A float-format number of the QoI obtained using
        mean input paramters
    
    sample: numpy.ndarray
        A multidimensional array that can be squeezed to two
        dimensions

    stats_name: str
        The label of the Quantity of Interest of which
        the convergence behavior is plotted

    n_draws: int
        Number of draws used to obtained the sample as part
        of the Monto Carlo Uncertainty Quantification

    color: str
        String that sets the Color of the convergence plot
        line

    Returns
    -------
    plt: Figure
        Returns Figure object setting figure-level attributes

    Notes
    -----
        The plt.text that sets QoI label on the right of the plot
        must be adjusted for smaller or very large draws.

    """

    # Delete superfluous array dimensions
    pre_df = np.squeeze(sample, axis=None)
    
    # Create column that computes the mean of all samples
    # until draw (which equals index plus one)
    df = pd.DataFrame(pre_df, columns=[stat_name]) 
    df[stat_name] = df[stat_name] - real_mean
    df['cum_sum_means'] = df[stat_name].cumsum()
    df['idx_plus_one'] = df.index.to_series() + 1
    df['mean_of_means'] = df['cum_sum_means']/df['idx_plus_one']  
         
    # Commonly ~1.33x wider than tall: (10, 7.5) or (12, 9)    
    plt.figure(figsize=(12, 9))    
      
    # Remove the plot frame lines.    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)        
    ax.spines["right"].set_visible(False)    
      
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()    
      
    # Limit the range of the plot to only where the data is.    
    # Avoid unnecessary whitespace.    
    plt.ylim(np.mean(df['mean_of_means']) - 0.66*abs(np.min(df['mean_of_means'])-np.max(df['mean_of_means'])),
    np.mean(df['mean_of_means']) + 0.66*abs(np.min(df['mean_of_means'])-np.max(df['mean_of_means'])))
    plt.xlim(1, n_draws)    
      
    # Ensure axis ticks are large enough to be easily read.    
    plt.yticks(fontsize=14)    
    plt.xticks(fontsize=14)    
      
    # Provide tick lines across the plot to help viewers trace along    
    # the axis ticks.
    ax = plt.gca()
    ax.yaxis.grid(which='major', linestyle='--', lw=0.5, color="black", alpha=0.3)          
    
    # Plot draws and mean of means until draw     
    plt.plot(df.index,    
            df['mean_of_means'].values,    
            lw=2.5, color=color, label=stat_name)

    # Add data label to legend
    lgd = plt.legend(
        fontsize=16, edgecolor='white', handlelength=0,
        bbox_to_anchor=(1.01,0.39), loc="lower right",
        framealpha=0.0)
    # Set legend text to plot color
    plt.setp(lgd.get_texts(), color=color)
    # For the future: Impove these lines:
    #Add a text label to the right end of every line.
    #y_pos = df['mean_of_means'].values[-1]    
    #plt.text(n_draws + 5, y_pos, stat_name, fontsize=18, color=color) 

    # Make sure that all labels are large enough   
    plt.ylabel("Deviation", fontsize=18, labelpad=14)
    plt.xlabel("Number of Random Draws", fontsize=18, labelpad=14)
      
    return plt