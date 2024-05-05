import os
import subprocess

import pandas as pd
from tqdm import tqdm

from Merge import Merge


def get_branch(right, pos, d):
    value = right[pos + d].strip()
    if 'https' in value:
        value = right[pos + d * 3].strip()
    return value


def get_no_request_merges(merges: list[Merge]) -> list:
    os.chdir('/csse/users/dlo54/Desktop/seng401/ass2/team-1000')  #
    # 'git', 'log', "--pretty=format:%h %p %d", '--decorate'
    process = subprocess.Popen(['git', 'log', '--oneline', '--decorate', '--merges'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    temp = []
    for text in process.stdout:
        # TODO make this work. (currently gets the parents.)
        parts = text.replace("'", '').split(' Merge')
        if len(parts) < 2:
            temp.append((parts[0], '', ''))
            continue

        right = parts[1].split(' ')
        pos = -1
        for i in range(len(right)):
            if right[i] == 'into':
                pos = i
        if pos == -1:
            continue
        f = get_branch(right, pos, - 1)
        t = get_branch(right, pos, + 1)
        if f == 'dev' or f == 'main' or f == 'origin/dev' or f == 'origin/main':
            continue
        if 'origin/' + f == t or 'origin/' + t == f or f == t:
            continue

        temp.append((parts[0], f, t))

    process = subprocess.Popen(['git', 'log', "--pretty=format:%h %p"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    par_to_child = dict()
    for text in process.stdout:
        parts = text.split(' ')
        if len(parts) > 2:
            par1 = parts[1].strip()
            par2 = parts[2].strip()
            child = parts[0].strip()
            if par1 not in par_to_child:
                par_to_child[par1] = {child}
            else:
                par_to_child[par1].add(child)

            if par2 not in par_to_child:
                par_to_child[par2] = {child}
            else:
                par_to_child[par2].add(child)
        else:
            par = parts[1].strip()
            child = parts[0].strip()
            if par not in par_to_child:
                par_to_child[par] = {child}
            else:
                par_to_child[par].add(child)
    print(par_to_child)
    mr_commits = set()
    for merge in merges:
        oid = merge.get_commit()['short_id']
        if oid not in par_to_child:
            continue
        mr_commits.update(par_to_child[oid])
    print(mr_commits)
    commits = []
    froms = []
    tos = []

    for parts in tqdm(temp):
        oid = parts[0].split(' ')[0]
        print(oid)
        if all(m != oid for m in mr_commits):
            commits.append(oid)
            froms.append(parts[1])
            tos.append(parts[2])

    df_frame = pd.DataFrame({
        'commit': commits,
        'from': froms,
        'to': tos
    })
    os.chdir('/csse/users/dlo54/Desktop/seng401/ass2')
    df_frame.to_csv('not_reqeasted.csv', index=False)
