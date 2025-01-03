
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

PARENT_DIR = os.path.abspath(os.path.dirname(__file__))

def write_pca_in_amber_cpptraj(pca_in_filepath, num_residues):

    with open(pca_in_filepath, 'w') as f:
        f.write(
f'parm nowat.prmtop\n\
trajin nowat.dcd\n\
rms first :1-{num_residues}&!@H=\n\
matrix covar name MyMatrix :1-{num_residues}&!@H=\n\
createcrd CRD1\n\
run\n\
runanalysis diagmatrix MyMatrix vecs 2 name MyEvecs\n\
crdaction CRD1 projection evecs MyEvecs :1-{num_residues}&!@H= out pca_2d.dat beg 1 end 2\n\
quit\n'
        )

def amberpca2gmxpca(pcadata_path, out_path):
    with open(pcadata_path,'r') as fr:
        lines = fr.readlines()
        with open(out_path,'w') as fw:
            fw.write('@TYPE xy\n')
            for line in lines:
                if not line.startswith('#'):
                    words = line.strip().split()
                    fw.write('  '+str(float(words[1]))+'   '+str(float(words[2]))+'\n')

def ddtpd(input_path):
    """
    need process
    """
    os.chdir(os.path.dirname(input_path))
    os.system('ddtpd.exe {} 100 100 2 y y'.format(input_path))


def ddtpd2matrix(dpptd_path):
    ls = []
    with open(dpptd_path,'r') as f:
        lines = f.readlines()
        for line in lines:
            words = line.strip().split()
            ls.append([float(words[0]),float(words[1]),float(words[2]),])
    df = pd.DataFrame(ls)
    df.columns = ['PCA1','PCA2','value']
    return df


def ddtpd2frame(pca_2d_path='project_fix.dat', pca_3d_path='result2.txt', extract_coordinate_path='extract_coordinate.txt', extract_frame_in_path='extract_frame.in'):
    file1 = pd.read_csv(pca_2d_path,sep='\s+',header=0)
    file1.columns = ['A','B']
    file2 = pd.read_csv(pca_3d_path, header=None, sep='\s+')
    file2.columns = ['X','Y','Z']

    def find_top(file2, top):
        top_min_indices = file2['Z'].nsmallest(top).index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y', 'Z']].values
        return top_min_values
    
    def find_0(file2):
        top_min_indices = file2[file2['Z']==0].index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y', 'Z']].values
        return top_min_values

    def find_dbscan(file2):
        db = DBSCAN(eps=5, min_samples=3)
        file2 = file2[file2['Z'] < 1]
        file2['cluster'] = db.fit_predict(file2[['X', 'Y']])
        min_z_points = []
        for cluster_label in file2['cluster'].unique():
            if cluster_label == -1:
                continue
            cluster_data = file2[file2['cluster'] == cluster_label]
            min_z_idx = cluster_data['Z'].idxmin()
            min_z_point = cluster_data.loc[min_z_idx, ['X', 'Y', 'Z']]
            min_z_points.append(min_z_point)
        return min_z_points
    
    def find_kmeans(file2, n_clusters=3):
        file2 = file2[file2['Z'] < 1]
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        file2['cluster'] = kmeans.fit_predict(file2[['X', 'Y']])
        min_z_points = []
        for cluster_label in file2['cluster'].unique():
            cluster_data = file2[file2['cluster'] == cluster_label]
            min_z_idx = cluster_data['Z'].idxmin()
            min_z_point = cluster_data.loc[min_z_idx, ['X', 'Y', 'Z']]
            min_z_points.append(min_z_point)
        return min_z_points


    matching_indices = []
    top_min_values = find_kmeans(file2, n_clusters=3)
    for value in top_min_values:
        x, y, z = value
        distances = np.sqrt((file1['A'] - x) ** 2 + (file1['B'] - y) ** 2)
        min_index = distances.idxmin()
        matching_indices.append(min_index)

    with open(extract_coordinate_path,'w') as f:
        f.write('Frame\tX\tY\tZ\n')
        for i,index in enumerate(matching_indices):
            f.write('{}\t{}\t{}\t{}\n'.format(index+1,top_min_values[i][0],top_min_values[i][1],top_min_values[i][2]))

    with open(extract_frame_in_path,'w') as f:
        f.write('parm nowat.prmtop\n')
        for index in matching_indices:
            f.write('trajin nowat.dcd {} {}\ntrajout frame_{}.pdb pdb\nrun\nclear trajin\n'.format(index+1,index+1,index+1))
        f.write('quit\n')



TITLE_FONT = {'family':'Arial', 'size':16, 'fontweight':'bold'}
LABEL_FONT = {'family':'Arial','size':12,'fontweight':'bold'}
TICKSLABEL_FONT = {'family':'Arial','size':8,'fontweight':'bold'}
LEGEND_FONT = {'labelfontfamily':'Arial','labelsize':12,'width':1}
SS_DIC = {"None":0,"Ext":1,"Bridge":2,"3-10":3,"Alpha":4,"Pi":5,"Turn":6,"Bend":7}

cmap_original = plt.cm.get_cmap('RdYlBu')
colors = cmap_original(np.linspace(0, 0.95, 256)) 
new_cmap = LinearSegmentedColormap.from_list("truncated_RdBu", colors)

def plot_pca_3d(df, name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X = np.array(df['PCA1']).reshape(int(len(df['PCA1'])**0.5),int(len(df['PCA1'])**0.5))
    Y = np.array(df['PCA2']).reshape(int(len(df['PCA2'])**0.5),int(len(df['PCA2'])**0.5))
    Z = np.array(df['value']).reshape(int(len(df['value'])**0.5),int(len(df['value'])**0.5))
    max_z = np.max(Z)
    min_z = np.min(Z)
    offset = min_z - (max_z-min_z)/3
    ax.plot_trisurf(X.flatten(), Y.flatten(), Z.flatten(), cmap=new_cmap, linewidth=1)
    ax.contourf(X, Y, Z, zdir='z', offset=offset, cmap=new_cmap)
    ax.set_xlabel('PCA1',fontdict=LABEL_FONT)
    ax.set_ylabel('PCA2',fontdict=LABEL_FONT)
    ax.set_zlabel('value',fontdict=LABEL_FONT,rotation=90)
    ax.set_zlim((offset,max_z))
    ax.view_init(elev=20,azim=-45)
    plt.tight_layout()
    plt.savefig(name+'_pca_3d.png', dpi=300)

def plot_pca2d(df, name):
    plt.scatter(df['PCA1'], df['PCA2'], c=df['value'], cmap='coolwarm', alpha=0.8)
    plt.colorbar(label='Values')
    plt.tight_layout()
    plt.savefig(name+'_pca_2d.png', dpi=300)

if __name__=='__main__':
    for sub in ['pca3d']:
        # amberpca2gmxpca('pca2d.dat','pca_2d_gmx.dat')
        # df = ddtpd2matrix('result2.txt')
        # plot_pca_3d(df,sub)
        ddtpd2frame('pca_2d_gmx.dat', 'result2.txt')
