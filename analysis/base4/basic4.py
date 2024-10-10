import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

TITLE_FONT = {'family':'Arial', 'size':20, 'fontweight':'bold'}
LABEL_FONT = {'family':'Arial', 'size':12, 'fontweight':'bold'}
LEGEND_FONT = {'family':'Arial', 'size': 8, 'weight': 'bold'}
TICKSLABEL_FONT = {'family':'Arial','size':8,'fontweight':'bold'}


def total_statistics(ls):
    min_,max_ = min(ls),max(ls)
    bins_mid = np.linspace(min_,max_,25)
    return min_,max_,bins_mid

def item_statisctics(ls,min_,max_):
    bins = pd.cut(ls,np.linspace(min_,max_,26))
    bins_num = bins.value_counts().sort_index().to_list()
    bins_freq = [100*_/len(ls) for _ in bins_num]
    return bins_freq

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

def plot_curve(ax,df,title,x_column='Frame',x_true=500,y_columns=['apo','Fulvestrant','Meropenem','Paliperidone','Sitagplitin','Lsavuconazonium'],colors=['black','red','blue','green','orange','purple','cyan'],xlabel='time (ns)',ylabel='RMSD (nm)',x_min=0,y_min=0,max_=None):
    custom_lines = []
    for i,y_column in enumerate(y_columns):
        ax.plot(df[x_column]/(len(df)/x_true),df[y_column],color=colors[i],linewidth=0.5,linestyle="-",label=y_column)
        custom_lines.append(Line2D([0], [0], color=colors[i], lw=1))
    ax.set_xlabel(xlabel,fontdict=LABEL_FONT)
    ax.set_ylabel(ylabel,fontdict=LABEL_FONT)
    x_ticks,minor = split_ticks(x_true)
    ax.set_xlim((x_min,x_true))
    ax.set_xticks(x_ticks)
    ax.set_ylim((y_min,max_+(max_-y_min)*0.4))
    major_locator = ticker.MultipleLocator(minor*2)
    minor_locator = ticker.MultipleLocator(minor)
    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.legend(custom_lines,y_columns,frameon=False,loc='upper left',prop=LEGEND_FONT)
    ax.set_title(title,x=-0.1,y=0.99,fontdict=TITLE_FONT)

def plot_frequency(ax,df,title,y_columns=['apo','Fulvestrant','Meropenem','Paliperidone','Sitagplitin','Lsavuconazonium'],colors=['black','red','blue','green','orange','purple','cyan'],xlabel='RMSD (nm)',ylabel='Relative Frequency (%)',bins_mid_=[],min_=None,max_=None):
    custom_lines = []
    for i,y_column in enumerate(y_columns):
        bins_freq = item_statisctics(df[y_column],min_,max_)
        print(y_column)
        ax.plot(bins_mid_,bins_freq,color=colors[i],linewidth=0.5,linestyle="-",label=y_column,marker='s',markersize=4)
        custom_lines.append(Line2D([0], [0], color=colors[i], lw=1))
    ax.set_xlabel(xlabel,fontdict=LABEL_FONT)
    ax.set_ylabel(ylabel,fontdict=LABEL_FONT)
    ax.legend(custom_lines,y_columns,frameon=False,loc='upper left',prop=LEGEND_FONT)
    ax.set_title(title,x=-0.1,y=0.98,fontdict=TITLE_FONT)


def plot_basic4():
    time = 500 #ns
    num_residue = 728 #aa
    # titles = ['(A)','(B)','(C)','(D)','(E)','(F)','(G)','(H)','(I)','(J)','(K)','(L)']
    titles = ['A','B','C','D','E','F','G','H','I','J','K','L']
    y_columns = ['apo','Fulvestrant','Meropenem','Paliperidone','Isavuconazonium']
    colors = ['black','red','blue','green','orange','purple','cyan']
    ylabels = ['RMSD (Å)','RMSF (Å)','Rg (Å)','SASA (Å\u00b2)']
    fig = plt.figure(figsize=(8,12), dpi=300) # figsize
    plt.rcParams['xtick.direction'] = 'in' 
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['xtick.major.width'] = 1.5
    for i,sub in enumerate(['RMSD','RMSF','Rg','SASA']):
        df = pd.read_excel('basic4_gamd.xlsx',sheet_name=sub) 
        ls = np.array(df.iloc[1:,1:]).flatten()
        min_,max_,bins_mid_ = total_statistics(ls)
        axa = fig.add_subplot(4,2,2*i+1)
        axb = fig.add_subplot(4,2,2*i+2)
        if sub != 'RMSF':
            if sub != 'RMSD':
                plot_curve(axa,df,title=titles[2*i],x_column='Frame',x_true=time,y_columns=y_columns,colors=colors,xlabel='Time (ns)',ylabel=ylabels[i],x_min=0,y_min=min_,max_=max_)
            else:
                plot_curve(axa,df,title=titles[2*i],x_column='Frame',x_true=time,y_columns=y_columns,colors=colors,xlabel='Time (ns)',ylabel=ylabels[i],x_min=0,y_min=min_,max_=max_)
        else:
            plot_curve(axa,df,title=titles[2*i],x_column='Residue',x_true=num_residue,y_columns=y_columns,colors=colors,xlabel='Residue No.',ylabel=ylabels[i],x_min=1,y_min=0,max_=max_)
        plot_frequency(axb,df,title=titles[2*i+1],y_columns=y_columns,colors=colors,xlabel=ylabels[i],ylabel='Relative Frequency (%)',bins_mid_=bins_mid_,min_=min_,max_=max_)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0., hspace=0.)
    plt.tick_params(pad=0.0)  
    plt.tight_layout()
    plt.savefig('basic4_gamd.png')
    
if __name__ == '__main__':
    plot_basic4()


