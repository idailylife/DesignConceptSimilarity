# -*- coding: utf-8 -*-
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

class SimilarityMat:
    """
    Reads similarity matrix from csv file and generate upper triangular array for Scipy.
    The array follows the format of the output of 'pdist' function, which is a 1-by-N*(N-1)/2 matrix (vector)
    """
    def __init__(self, csvFileName, na_val=0):
        self.mat = np.genfromtxt(csvFileName, delimiter=',')
        self.filename = csvFileName
        self.na_val = na_val

    def triangular_array(self, upper=True):
        mat = self.mat
        if not upper:
            mat = mat.T
        ret_ary = []
        for i in range(0, mat.shape[0]):
            for j in range(i, mat.shape[0]):
                ret_ary.append(mat[i][j])
        return ret_ary

    def set_na_val(self, val):
        self.mat[self.mat == 0] = val
        self.na_val = val

    def flip_neg(self):
        # flip negative value (log probability, higher is better) to positive distance (lower is better)
        self.mat = -self.mat


if __name__ == '__main__':
    simMat = SimilarityMat(r'E:\WordNet_Data\sentence_similarity_wordnet.csv')
    #print simMat.mat
    simMat.set_na_val(-5)
    simMat.flip_neg()
    triangular_ary = simMat.triangular_array()
    print triangular_ary
    # Hierarchy clustering
    linkage_mat = hierarchy.linkage(triangular_ary, method='ward')  # Each line reads  [idx, idx2, dist, sample_count]
    print linkage_mat
    fig = plt.figure(figsize=(100, 20))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    hierarchy.dendrogram(linkage_mat, leaf_rotation=90., leaf_font_size=8)
    plt.show()
    fig.savefig('output.png', dpi=600)