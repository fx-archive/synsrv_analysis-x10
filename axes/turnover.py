
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import mV, ms, second

import pickle

from methods.process_turnover import extract_lifetimes, \
                                     extract_active_synapse_count, \
                                     extract_delta_a_on_spike




def lifetime_distribution_loglog(ax, bpath, nsp, bins,
                                 discard_t, with_starters, label_key=''):
    ''' 
    discard all values until discard_t
    '''
    if discard_t!=0.:
        raise NotImplementedError
    else:
        print("not discarding any ts")


    with open(bpath+'/raw/turnover.p', 'rb') as pfile:
        turnover = pickle.load(pfile)


    if not len(turnover) == 0:
        
        _lt, _dt = extract_lifetimes(turnover, nsp['N_e'], with_starters=with_starters)
        life_t, death_t = _lt*second, _dt*second

        if len(life_t) == 0:
            print('No recorded lifetimes, not plotting distribution')
            ax.set_title('No recorded lifetimes')
        else:
            b_min, b_max = nsp['dt']/ms, np.max(life_t/ms)
            bins = np.linspace(np.log10(b_min), np.log10(b_max), bins)

            label = ''
            if label_key!='':
                label=  r'$\text{' + label_key +\
                        '} = %f $' %(getattr(tr, label_key))
                
            ax.hist(life_t/ms, 10**bins, log=True, density=True, label=label)

            ax.set_title('Lifetime distribution')
            ax.set_xlabel('time [ms]')
            ax.set_xscale('log')
            ax.set_xlim(b_min,b_max)

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')



def lifetime_distribution_loglog_linear_bins(ax, bpath, nsp, bin_w,
                                             discard_t, with_starters,
                                             label_key = '', n_color=0):
    ''' 
    discard all values until discard_t
    '''
    if discard_t!=0.:
        raise NotImplementedError
    else:
        print("not discarding any ts")


    with open(bpath+'/raw/turnover.p', 'rb') as pfile:
        turnover = pickle.load(pfile)


    if not len(turnover) == 0:
    
        _lt, _dt = extract_lifetimes(turnover, nsp['N_e'], with_starters)
        life_t, death_t = _lt*second, _dt*second

        counts, edges = np.histogram(life_t/ms,
                                     bins=np.arange(nsp['dt']/ms,nsp['T']/ms, bin_w/ms))
        centers = (edges[:-1] + edges[1:])/2.

        label = ''
        if label_key!='':
            label=  r'$\text{' + label_key +\
                    r'} = \text{'+'%.2E' %(Decimal(getattr(tr, label_key))) +\
                    r'}$'

        print('assuming fixed number of lines, n_color=5!')

        ax.plot(centers, counts, '.', markersize=2., label=label)#,
                #color=pl.cm.Greens(np.linspace(0.2,1,5)[n_color]))
        
            
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('synapse lifetimes (' + \
                 r'$\text{bin width} = \text{\SI{%d}{ms}}$)' % (int(bin_w/ms)))
    ax.set_xlabel('synapse lifetime [ms]')
    ax.set_ylabel('absolute occurrence')
            
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
            
