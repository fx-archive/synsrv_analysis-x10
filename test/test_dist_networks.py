
import unittest, os, time
from brian2.units import second
import numpy as np

# get tested
from methods.process_survival import  extract_survival


class Test_extract_survival(unittest.TestCase):



    def test_turnover_data_set1(self):
        t_split, t_cut, bin_w = 5*second, 2*second, 1*second
        turnover_data = [[1, 2.5, 0, 0]]

        full_t, ex_ids = extract_survival(np.array(turnover_data),
                                          bin_w, 10,
                                          t_split, t_cut)

        self.assertEqual(len(full_t),1)
        self.assertEqual(full_t[0],t_split/second)

        
    def test_turnover_data_speed(self):
        t_split, t_cut, bin_w = 4*second, 2*second, 1*second
        turnover_data = np.genfromtxt('test/test_sets/turnover_test_set1',
                                      delimiter=',')

        a = time.time()
        full_t, ex_ids = extract_survival(turnover_data,
                                          bin_w, 1000,
                                          t_split, t_cut)
        b = time.time()

        print('Test Set 1 took :', b-a, ' s')
        
        # self.assertEqual(len(full_t),1)
        # self.assertEqual(full_t[0],t_split/second)
        
    
#     positions = distribute_neurons_randomly(N, ed_l)     
#     xy = g.new_vertex_property("vector<double>")
#     for k in range(N):
#         g.add_vertex()
#         xy[g.vertex(k)] = list(positions[k])
#     g.vertex_properties["xy"] = xy

#     def test_all_to_all_connectivity(self):
#         d = lambda x: 1.
#         g = connect_dist_network(self.g, d)
#         self.assertEqual(g.num_edges(), self.N*(self.N-1))
#         self.g.clear_edges()
        
#     def test_none_to_none_connectivity(self):
#         d = lambda x: 0.
#         g = connect_dist_network(self.g, d)
#         self.assertEqual(g.num_edges(), 0)
#         self.g.clear_edges()



if __name__ == '__main__':
    unittest.main()
