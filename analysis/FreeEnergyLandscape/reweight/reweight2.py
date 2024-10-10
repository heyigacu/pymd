import subprocess
import os
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import KMeans

def read_first_column(filename):
    return pd.read_csv(filename, delimiter=' ', usecols=[0], header=None).squeeze()

def twofile_to_onefile(file1, file2, output_file):
    col1_file1 = read_first_column(file1)
    col1_file2 = read_first_column(file2)
    merged_columns = pd.concat([col1_file1, col1_file2], axis=1, ignore_index=True)
    merged_columns.to_csv(output_file, sep=' ', index=False, header=False)

def pca2d_to_inputfile(file, output_file):
    df = pd.read_csv(file, sep='\s+')
    df = df.iloc[:,1:3]
    df.to_csv(output_file, sep=' ', index=False, header=None)



def process_gamd_log(input_file, output_file, temperature, frame=5000):
    """
    Process the gamd.log file to compute values and save to output_file.
    Removes the first three lines of headers from the input file before processing.

    Parameters:
    input_file (str): Path to the input file (e.g., 'gamd.log').
    output_file (str): Path to the output file (e.g., 'weights.log').
    temperature (float): Temperature value to be used in the calculations.
    """
    
    # Remove the first three lines from the input file
    temp_file = 'temp_gamd.log'
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Write the data without the first three lines to a temporary file
    with open(temp_file, 'w') as outfile:
        outfile.writelines(lines[3:(3+frame)])
    
    # Read the temporary file without headers
    data = pd.read_csv(temp_file, delim_whitespace=True, header=None)
    
    # Extract the required columns (7th, 8th, and 2nd columns)
    col7 = data[6]  # 7th column
    col8 = data[7]  # 8th column
    col2 = data[1]  # 2nd column
    
    # Perform calculations
    result = (col7 + col8) / (0.001987 * temperature)
    
    # Create output DataFrame
    output = pd.DataFrame({
        'Result': result,
        'Col2': col2,
        'Sum': col7 + col8
    })
    
    # Save to the output file
    output.to_csv(output_file, sep=' ', index=False, header=False)


def extract_second_column(input_file, output_file):
    """
    Extracts the second column from the input file and saves it to the output file, excluding the header.

    Parameters:
    input_file (str): Path to the input file.
    output_file (str): Path to the output file.
    """
    # Read the input file, skipping the header
    df = pd.read_csv(input_file, delim_whitespace=True, header=0)
    
    # Extract the second column (index 1)
    second_column = df[df.columns[1]]
    
    # Save the second column to the output file
    second_column.to_csv(output_file, index=False, header=False)


def plot_2d(df, name='', xlabel='PCA1',ylabel='PCA2',title='apo',legend_label='PMF (kcal/mol)'):
    df['X'] = pd.to_numeric(df['X'], errors='coerce')
    df['Y'] = pd.to_numeric(df['Y'], errors='coerce')
    df['Z'] = pd.to_numeric(df['Z'], errors='coerce')
    df = df.dropna()
    X_unique = np.sort(df['X'].unique())
    Y_unique = np.sort(df['Y'].unique())
    X, Y = np.meshgrid(X_unique, Y_unique)
    Z = df.pivot_table(index='Y', columns='X', values='Z').values
    colors = ['blue','cyan','LimeGreen','yellow', 'red',   ]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)
    plt.figure()
    cp = plt.contourf(X, Y, Z, levels=20, cmap=cmap) 
    cbar = plt.colorbar(cp)  
    cbar.set_label(legend_label, fontsize=12, fontweight='bold') 
    plt.title(name, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12, fontweight='bold')
    plt.ylabel(ylabel, fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'pmf_c2_2d_{name}.png',dpi=300)

def run_python_scripts(name, Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T):
    # Get the current working directory
    workdir = os.getcwd()
    
    # Run the reweight-1d.sh script
    for data_1d in data_1ds:
        os.system(f'python PyReweighting-2D.py -input {data_1d} -T {T} -Emax {Emax} -cutoff {cutoff} -discX {binx} -discY {biny} -job amdweight_CE -weight weights.dat')
        os.system(f'python PyReweighting-1D.py -input {data_1d} -T {T} -Emax {Emax} -cutoff {cutoff} -discX {binx} -discY {biny} -job noweight')
    
    # Run the reweight-2d.sh script
    for data_2d in data_2ds:
        os.system(f'python PyReweighting-2D.py -input {data_2d} -T {T} -Emax {Emax} -cutoff {cutoff} -discX {binx} -discY {biny} -job amdweight_CE -weight weights.dat')
        df = pd.read_csv('pmf-c2-pca2d_.dat.xvg', sep='\t')
        df = df.iloc[3:, :]
        df.columns = ['X', 'Y', 'Z']
        plot_2d(df,name)
        # os.system(f'python PyReweighting-2D.py -input {data_2d} -T {T} -Emax {Emax} -cutoff {cutoff} -discX {binx} -discY {biny} -job noweight')

def generate_combinations(elements):
    """
    Generate all unique pairs (combinations of 2) from the given list of elements.

    Parameters:
    elements (list): A list of elements to generate pairs from.

    Returns:
    list: A list of tuples, where each tuple is a unique pair of elements.
    """
    # Generate all combinations of 2 elements
    pairs = list(combinations(elements, 2))
    
    return pairs

def pmf2frame(pca_2d_path='pca2d_.dat', pca_3d_path='pmf-c2-pca2d_.dat.xvg', extract_coordinate_path='extract_coordinate.txt', extract_frame_in_path='extract_frame.in', find0=False):
    file1 = pd.read_csv(pca_2d_path,sep='\s+',header=0)
    file1.columns = ['A','B']
    file2 = pd.read_csv(pca_3d_path, sep='\t')
    file2 = file2.iloc[3:, :]
    file2.columns = ['X', 'Y', 'Z']

    def find_top(top):
        top_min_indices = file2['Z'].nsmallest(top).index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y', 'Z']].values
        return top_min_values
    
    def find_0():
        top_min_indices = file2[file2['Z']==0].index
        top_min_values = file2.loc[top_min_indices, ['X', 'Y', 'Z']].values
        return top_min_values

    def find_lower(df, n_clusters=3):
        kmeans = KMeans(n_clusters=n_clusters)
        df['cluster'] = kmeans.fit_predict(df[['X', 'Y']])
        lowest_xy = []
        for cluster in range(n_clusters):
            cluster_data = df[df['cluster'] == cluster]
            min_z_idx = cluster_data['Z'].idxmin()
            lowest_point = df.loc[min_z_idx, ['X', 'Y', 'Z']].values
            lowest_xy.append(lowest_point)
        return lowest_xy

    if find0:
        lower = find_0()
    else:
        lower = find_lower(file2, n_clusters=4)

    matching_indices = []
    for value in lower:
        x, y, z = value
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            print(f"无法将 x 或 y 转换为浮点数: x={x}, y={y}")
            continue  # 跳过这个值，继续下一个

        # 将 A 和 B 列转换为数值类型（如果尚未转换）
        file1['A'] = pd.to_numeric(file1['A'], errors='coerce')
        file1['B'] = pd.to_numeric(file1['B'], errors='coerce')
        distances = np.sqrt((file1['A'] - x) ** 2 + (file1['B'] - y) ** 2)
        min_index = distances.idxmin()
        matching_indices.append(min_index)

    top_min_values = lower
    print(top_min_values)
    print(file1.iloc[matching_indices,:])
    print("Matching indices in file1 for the smallest three values in file2:", matching_indices)

    with open(extract_coordinate_path,'w') as f:
        f.write('Frame\tX\tY\tZ\n')
        for i,index in enumerate(matching_indices):
            f.write('{}\t{}\t{}\t{}\n'.format(index+1,top_min_values[i][0],top_min_values[i][1],top_min_values[i][2]))

    with open(extract_frame_in_path,'w') as f:
        f.write('parm nowat.prmtop\n')
        for index in  matching_indices:
            f.write('trajin nowat.dcd {} {}\ntrajout frame_{}.pdb pdb\nrun\nclear trajin\n'.format(index+1,index+1,index+1))
        f.write('quit\n')

# Example usage
if __name__ == "__main__":
    name = 'apo'
    input_file = 'gamd.log'
    output_file = 'weights.dat'
    Emax = 100
    cutoff = 1
    binx = 12
    biny = 12
    binz = 2
    T = 310
    # pca2d_to_inputfile('pca2d.dat','pca2d_.dat')
    # process_gamd_log(input_file, output_file, T, frame=5000)
    searched = False
    if searched:
        searched_fileds = ['rmsd', 'dis']
        searched_1d = []
        for filed in searched_fileds:
            extract_second_column(filed+'.dat', filed+'_.dat')
            searched_1d.append(filed+'_.dat')
        pairs = generate_combinations(searched_fileds)
        searched_2d = []
        for pair in pairs:
            filed1, filed2 = pair
            twofile_to_onefile(f'{filed1}_.dat',f'{filed2}_.dat',f'{filed1}{filed2}.dat')
            searched_2d.append(f'{filed1}{filed2}.dat')
        data_1ds = searched_1d
        data_2ds = searched_2d
        data_3ds = []
        run_python_scripts(name, Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T)

    else:
        data_1ds = []
        data_2ds = ['pca2d_.dat']
        data_3ds = []        
        run_python_scripts(name,Emax, cutoff, binx, biny, binz, data_1ds, data_2ds, data_3ds, T)
        pmf2frame()
