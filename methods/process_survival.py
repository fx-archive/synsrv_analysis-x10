
from brian2.units import second
import sys, time
import numpy as np
import pandas as pd

def extract_survival(turnover_data, bin_w, N_neuron, t_split,
                      t_cut = 0.*second):
    '''
    turnover data is assumed to be a numpy.array with 
    lines consisting of the four entries
    
      gen/prune, t, i, j     

    where 
      -- gen/prune :: 1 if synapse became active, 
                      0 if synapse became inactive
      -- t         :: simulation time point in seconds(!)
      -- i         :: pre-synaptic neuron index
      -- j         :: post-synaptic neuron index

    -----------

    parameters:
     
     -- turnover_data  :: 
     -- N_neuron       ::
     -- t_split        :: 

                          
    returns: 

     # -- lifetimes  :: duration from generation (or initial presence) 
     #                  until pruning. Synapses generated (initally 
     #                  present) but not yet pruned at simulation end 
     #                  are NOT INCLUDED
     # -- deathtimes :: like lifetimes, but from death to generation,
     #                  i.e. time from begining of simulation until 
     #                  first generation is not included 
    '''

    # array([[  1.,   0.,   2., 347.],
    #        [  1.,   0.,   3., 248.],
    #        [  1.,   0.,   4., 145.],
    #        [  1.,   0.,  14., 210.],
    #        [  1.,   0.,  20., 318.]])
    #

    t_split, t_cut, bin_w = t_split/second, t_cut/second, bin_w/second
    
    survival_times = np.arange(0, t_split+bin_w, bin_w)
    survival_times = survival_times*second

    full_t = []

    a = time.time()
    turnover_data = turnover_data[turnover_data[:,1]>= t_cut]
    turnover_data[:,1] = turnover_data[:,1]-t_cut
    b = time.time()
    print('cutting took %.2f seconds' %(b-a))


    df = pd.DataFrame(data=turnover_data, columns=['struct', 't', 'i', 'j'])

    df = df.astype({'struct': 'int64', 'i': 'int64', 'j': 'int64'})

    df['s_id'] = df['i'] * 1000 + df['j']

    df = df.sort_values(['s_id', 't'])

    excluded_ids = []
    
    for s_id, gdf in df.groupby('s_id'):

        if len(gdf) == 1:
            if gdf['struct'].iloc[0]==1 and gdf['t'].iloc[0]<=t_split:
                # synapses started but did not die with sim tim
                # add maximal survival time t_split
                full_t.append(t_split)
            else:
                # the cases are:
                #  -- synapse was present at beginning and died
                #  -- synapse grew but we don't have enough time
                #     data to track it's full survival
                #
                # we're not adding in these cases
                pass

        elif len(gdf) > 1:

            # we need to test that...
            tar = np.abs(np.diff(gdf['struct']))

            if np.sum(tar)!=len(tar):
                excluded_ids.append(s_id)

            else:

                if gdf['struct'].iloc[0] == 0:
                    # dies first, get rid of first row
                    gdf = gdf[1:]

                if len(gdf)==1 and gdf['t'].iloc[0]<=t_split:
                    # synapses started but did not die with sim tim
                    # add maximal survival time t_split
                    full_t.append(t_split)

                elif len(gdf)>1 and gdf['t'].iloc[0]<=t_split:

                    # only if first growth event is before t_split
                    # otherwise not enough time to potentially
                    # long surviving synapses
                  
                    # normalize to the times of the first growth event
                    # +gdf['t'] = gdf['t']-gdf['t'].iloc[0]+
                    # --> done below by adding to t_split

                    # filter out events after window t_split
                    gdf_cut = gdf[gdf['t'] <= t_split+gdf['t'].iloc[0]]

                    # starts with growth and ends on pruning event
                    if len(gdf_cut) % 2 == 0:

                        srv_t = np.diff(gdf_cut['t'])
                        assert np.max(srv_t)<=t_split

                        full_t.extend(list(srv_t)[::2])

                    # ends on growth event, need to find next pruning event
                    elif len(gdf_cut) % 2 == 1:

                        if len(gdf_cut) == 1:
                            
                            if len(gdf_cut) == len(gdf):
                                # can't find any, add maximal survival
                                full_t.append(t_split)

                            else:
                                print(gdf_cut)
                                print(gdf)
                                full_t.append(gdf['t'].iloc[len(gdf_cut)] - \
                                              gdf_cut['t'].iloc[0])  
                                
                                
                                
                    #     else:
                    #         c_sort_appendix = c_sort[len(c_sort_cut),:]
                    #         # try:
                    #         #     assert c_sort_appendix[0]==0
                    #         # except AssertionError:
                    #         #     print("c_sort: ", c_sort)
                    #         #     print("c_sort_cut: ", c_sort_cut)
                    #         #     print("c_sort_appendix: ", c_sort_appendix)
                    #         #     assert False
                    #         #     assert c_sort_appendix[0]==0
                    #         #     sys.exit()

                    # #         c_sort_cut = np.vstack((c_sort_cut,
                    # #                                 c_sort_appendix))

                    # #         assert len(c_sort_cut) % 2 ==0

                    # #         lts = np.diff(c_sort_cut[:,1])

                    # #         for lt in lts:
                    # #             # look up lt in survival_bins
                    # #             # and add survival counts
                    # #             added_counts = np.zeros_like(survival_counts)
                    # #             added_counts[survival_times/second<lt]=1

                    # #             survival_counts += added_counts


# -------------------------------------------------                            
                                    
         


    b = time.time()
    print('main loop took %.2f seconds' %(b-a))

    # print('Excluded: ', exclude_count)
    
    return full_t, excluded_ids


