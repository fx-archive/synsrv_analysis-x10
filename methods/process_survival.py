
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
     -- initial        :: determines handling of initially at 
                          t_cut present synapsese

                          - "only" :: returns lifetimes only 
                              for synapses present at t_cut
                          - "with" :: return lifetimes of 
                              synapses present at t_cut and 
                              those generated after t_cut
                          - "without" :: return lifetimes of
                              synapses generated after t_cut      
      
    returns: 

     -- lifetimes  :: duration from generation (or initial presence) 
                      until pruning. Synapses generated (initally 
                      present) but not yet pruned at simulation end 
                      are NOT INCLUDED
     -- deathtimes :: like lifetimes, but from death to generation,
                      i.e. time from begining of simulation until 
                      first generation is not included 
    '''

    # lexsort by pre- and post-synaptic indices
    # Example:
    #
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

    exclude_ids = 0
    
    for s_id, gdf in df.groupby('s_id'):
    
        c_array = np.array(current_synapse)
        ind = np.argsort(c_array[:,1])
        c_sort = c_array[ind]

        elif len(gdf) == 1:
            if gdf['struct'].iloc[0]==1 and gdf['t'].iloc[0]<=t_split:
                # synapses started but did not die with sim tim
                # add maximal survival time t_split
                full_T.append(t_split)
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
                exclude_ids.append(s_id)

            else:

                if gdf['struct'].iloc[0] == 0:
                    # dies first, get rid of first row
                    gdf = gdf[1:]

                if len(gdf)==1 and gdf['t'].iloc[0]<=t_split:
                    # synapses started but did not die with sim tim
                    # add maximal survival time t_split
                    full_T.append(t_split)

                elif len(gdf) > 1:
                    pass
                    # # normalizes the times to the growth event
                    # c_sort[:,1] = c_sort[:,1]-c_sort[0,1]

                    # # filter out events after window t_split
                    # c_sort_cut = c_sort[c_sort[:,1]<=t_split/second]

                    # if len(c_sort_cut) % 2 == 0:
                    #     # ends on pruning event
                    #     lts = np.diff(c_sort_cut[:,1])
                    #     assert np.max(lts)<=t_split/second

                    #     for lt in lts:
                    #         # look up lt in survival_bins
                    #         # and add survival counts
                    #         added_counts = np.zeros_like(survival_counts)
                    #         # print(added_counts)
                    #         # print(added_counts[survival_times/second<lt])
                    #         added_counts[survival_times/second<lt]=1

                    #         survival_counts += added_counts

                    # elif len(c_sort_cut) % 2 == 1:
                    #     # ends on growth event find next death event
                    #     if len(c_sort_cut) == len(c_sort):
                    #         # can't find any, add maximal survival
                    #         survival_counts += np.ones_like(survival_counts)
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

                    #         c_sort_cut = np.vstack((c_sort_cut,
                    #                                 c_sort_appendix))

                    #         assert len(c_sort_cut) % 2 ==0

                    #         lts = np.diff(c_sort_cut[:,1])

                    #         for lt in lts:
                    #             # look up lt in survival_bins
                    #             # and add survival counts
                    #             added_counts = np.zeros_like(survival_counts)
                    #             added_counts[survival_times/second<lt]=1

                    #             survival_counts += added_counts


# -------------------------------------------------                            
                                    
         


    b = time.time()
    print('main loop took %.2f seconds' %(b-a))

    # print('Excluded: ', exclude_count)
    
    return full_t, excluded_ids


