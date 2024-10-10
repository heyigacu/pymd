import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
PARENT_DIR = os.path.abspath(os.path.dirname(__file__)) 


TITLE_FONT = {'family':'Arial', 'size':16, 'fontweight':'bold'}
LABEL_FONT = {'family':'Arial','size':14,'fontweight':'bold'}
TICKSLABEL_FONT = {'family':'Arial','size':10,'fontweight':'bold'}
LEGEND_FONT = {'labelfontfamily':'Arial','labelsize':12,'width':1}
color_list = [ 'aliceblue','#F3E1AF','#ADFF2F','purple','darkgreen','cyan','#507AAF','red']
SS_DIC = {"None":0,"Para β-sheet":1,"Anti-para β-sheet":2,"3-10 helix":3,"Alpha helix":4,"Pi helix":5,"Turn":6,"Bend":7}


def split_ticks(x_max):
    scientific_notation = '{:.3e}'.format(x_max)
    head = float(scientific_notation.split('e')[0])
    tail = int(scientific_notation.split('e')[1])
    if head > 5:
        return list(range(0,x_max,10**tail))+[x_max], 10**tail
    elif 5>= head >= 3.5:
        return list(range(0,x_max,5*10**(tail-1)))+[x_max], int(5*10**(tail-1))
    else:     
        return list(np.linspace(0,round(head)*10**tail,11).astype(int))[:-1]+[x_max], int(round(head)*10**tail/10)

def gnu2matrix(dsspgnu_path,max_true=500):
    with open(os.path.join(PARENT_DIR,dsspgnu_path),'r') as f:
        dic = {}
        lines = f.readlines()
        temp_residue = 0
        for line in lines:
                if line.strip()!='':
                    if line.strip()[0].isdigit():
                        words = line.strip().split()
                        if int(float(words[0])) != temp_residue:
                            temp_residue = int(float(words[0]))
                            dic[int(float(words[0]))] = {}
                            dic[int(float(words[0]))][int(float(words[1]))] = int(float(words[2].strip()))
                        elif int(float(words[0])) == temp_residue:
                            dic[int(float(words[0]))][int(float(words[1]))] = int(float(words[2].strip()))
                        else:pass
        df = pd.DataFrame(dic).iloc[:-1,:-1]
        # df.columns = [_*(max_true/df.shape[1]) for _ in df.columns]
        return df
    
def plot_matrix(df,name='apo',max_true=500,):
    fig = plt.figure(figsize=(10,5),dpi=300)
    ax = fig.add_subplot(1,1,1)
    cmap = sns.color_palette(color_list)
    sns.heatmap(df,cmap=cmap,ax=ax) 
    xticks,minor = split_ticks(df.shape[1])
    yticks,minor = split_ticks(df.shape[0])
    xticks[0] = 1
    yticks[0] = 1
    xticks_label = [int(_*(max_true/df.shape[1])) for _ in xticks]
    ax.set_title('Dictionary of Protein Secondary Structure',fontdict=TITLE_FONT)
    ax.set_xticks(xticks,xticks_label,rotation=0,fontdict=TICKSLABEL_FONT)
    ax.set_yticks(yticks,yticks,fontdict=TICKSLABEL_FONT)
    ax.invert_yaxis()
    ax.set_ylabel('Residue No.',fontdict=LABEL_FONT)
    ax.set_xlabel('Times (ns)',fontdict=LABEL_FONT)
    cbar = ax.collections[0].colorbar
    cbar.set_ticklabels(list(SS_DIC.keys())) 
    cbar.set_ticks(np.arange(0.5,7.5,7/8))
    cbar.ax.tick_params(**LEGEND_FONT)
    plt.tight_layout()
    plt.savefig(os.path.join(PARENT_DIR,name+'_dssp.png'))

def plot_dssp(dsspgnu_path=os.path.join(PARENT_DIR,'apo\\dssp.gnu'),name='apo'):
    df = gnu2matrix(dsspgnu_path)
    plot_matrix(df,name=name)
    row_counts = df.apply(pd.value_counts, axis=1).fillna(0)
    row_counts.to_csv(dsspgnu_path+'-counts.txt',index=False)
    

if __name__ == '__main__':

    plot_dssp('dssp.gnu')
        # plot_dssp(os.path.join(PARENT_DIR,f'{sub}\\dssp\\dssp.gnu'),sub)
        # plot_dssp(os.path.join(PARENT_DIR,f'{sub}\\dssp\\dssp.gnu'),sub)
        # plot_dssp(os.path.join(PARENT_DIR,f'{sub}\\dssp\\dssp.gnu'),sub)