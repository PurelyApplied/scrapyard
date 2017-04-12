#!/usr/bin/python3

from partitioning import Partitioning
from math import log
import logging

def get_index_communities(n, n_comm):
    '''Returns SBM-style community blocks.'''
    width = n // n_comm
    return [set(range(i * width, (i+1) * width)) for i in range(n_comm)]

def infer_index_communities(P : Partitioning):
    '''Returns SBM-style community blocks after inferring agent and community count.'''
    return get_index_communities(P.vertices(), len(P.part))



def rmat_communities(n, minimum_size=1,
                     num_initial_division : "0 means the whole graph is the first 'community'" =0):
    current_community_count = 2**num_initial_division
    communities = []
    logging.debug('n = {}, min size = {}, initial division = {}'.format(n, minimum_size, num_initial_division))
    while minimum_size <= n // current_community_count:
        logging.debug("Enter loop, current community count = {}".format(current_community_count))
        to_add = get_index_communities(n, current_community_count)
        logging.debug("Adding {} new communities.".format(len(to_add)))
        communities.extend(to_add)
        current_community_count *= 2
    return communities


def write_communities(Cs, filename, separator=" ", width=1):
    '''width = 0 infers width, which could be time consuming.'''
    if not width:
        width = max(max(len(str(v)) for v in c) for c in Cs) + 1
    buff = ''
    for c in Cs:
        buff += separator.join("{{:<{}d}}".format(width).format(v) for v in c) + "\n"
    if filename is not None:
        with open(filename, 'w') as o:
            o.write(buff)
    else:
        print(buff)

def load_communities(filename, seperator=None, target_type=int):
    '''seperator=" " breaks on formatted multispaces.  None provides
standard behavior of split() on whitespace.'''
    with open(filename) as s:
        return [
            {target_type(c) for c in line.split(seperator)}
            for line in s
            if line.strip() and line.strip()[0] != "#"]

####################
## My graph generation scripts below.


## Old good graph functions
def draw_comm_count_test(df, back_style="--", col='score', outfile=None, annotate=True, **kwargs):
    plt.figure(figsize=(12,8))
    for i in range(1, 7):
        plt.subplot(2, 3, i)
        k = 2**i
        df_to_plot_over_replicate(
            df[df.generator=="simple-er-{}".format(k)],
            col,
            back_style=back_style,
            outfile=None, show=False,
            annotate=annotate,
            **kwargs)
    if outfile:
        plt.savefig(outfile)



def full_draw_code_test(df, back_style='--', col='score', **kwargs):
    for g in GRAPHS:
        for score in ('all', 'top5000'):
            if g == GRAPHS[0] and score == 'top5000':
                continue
            logging.info(
                "Considering graph {!r} under community {!r}".format(
                    g, score))
            draw_code_test(df[df.generator == g][df.community_base == score],
                           back_style=back_style, col=col,
                           title="{}; ground {}".format(g, score),
                           **kwargs)
