import plotly.graph_objects as go
import numpy as np
from scipy.stats import beta

def get_beta_dist(alpha1, beta1, alpha2, beta2, film_name1, film_name2):
    #get beta distribution
    posterior_film1 = beta(alpha1*100,beta1*100) #beta distribution film1
    film1_samples = posterior_film1.rvs(5000) #sampling the distribution to get the likelihood for film1

    posterior_film2 = beta(alpha2*100,beta2*100) #beta distribution film2
    film2_samples = posterior_film2.rvs(5000) #sampling the distribution to get the likelihood for film2
    
    #initiate graph
    line = np.linspace(min([min(film1_samples),min(film2_samples)]),max([max(film1_samples),max(film2_samples)]),1000)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line,y=posterior_film1.pdf(line),
                             name=f'{film_name1} ratings PDF',
                             fill="tozeroy"))
    fig.add_trace(go.Scatter(x=line,y=posterior_film2.pdf(line),
                             name=f'{film_name2} ratings PDF',
                             fill="tozeroy"))

    fig.update_yaxes(visible=True, showticklabels=False)
    fig.update_xaxes(visible=True, showticklabels=False)

    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1
                                  ))

    
    #probablitiy each film outperform/having higher ratings compared to other
    probability_1_more_than_2 = np.mean(film1_samples > film2_samples)
    probability_2_more_than_1 = np.mean(film2_samples > film1_samples)

    return fig, probability_1_more_than_2, probability_2_more_than_1