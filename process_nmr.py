#!/usr/bin/env python


residues = 'ACDEFGHIKLMNPQRSTVWY'

amide_protons = {(res, 'H'): 'H' for res in residues}

methyl_protons = {
        ('A', 'HB'): 'CB',
        ('V', 'HG1'): 'CG1',
        ('V', 'HG2'): 'CG2',
        ('L', 'HD1'): 'CD1',
        ('L', 'HD2'): 'CD2',
        ('I', 'HD1'): 'CD1',
        ('I', 'HG1'): 'CG1',
        ('I', 'HG2'): 'CG2',
        }

side_chain_protons = {
        ('N', 'HD21'): 'HD21',
        ('N', 'HD22'): 'HD22',
        ('Q', 'HE21'): 'HE21',
        ('Q', 'HE22'): 'HE22',
        }

name_map = {}
name_map.update(amide_protons)
name_map.update(methyl_protons)
name_map.update(side_chain_protons)


def get_residue_mapping(sequence, res_id, atom_name):
    res_type = sequence[res_id - 1]
    new_name = name_map[(res_type, atom_name)]

    if new_name == atom_name:
        correction = 0.0
    else:
        correction = 1.0

    return new_name, correction


def map_to_heavy(sequence, res_i, res_j, name_i, name_j, dist):
    name_i, correction_i = get_residue_mapping(sequence, res_i, name_i)
    name_j, correction_j = get_residue_mapping(sequence, res_j, name_j)

    return name_i, name_j, dist + correction_i + correction_j


def get_groups():
    groups = []
    current_group = []

    with open('nonAmbiR.dat') as nmr_file:
        for line in nmr_file:
            line = line.strip()

            if line:
                current_group.append(line)
            else:
                groups.append(current_group)
                current_group = []
        groups.append(current_group)
    return groups


def fix_groups(groups, sequence):
    out_groups = []
    for g in groups:
        out = []
        for line in g:
            cols = line.split()
            res_i = int(cols[0])
            res_j = int(cols[1])
            dist = float(cols[3])
            name_i = cols[4]
            name_j = cols[5]

            name_i, name_j, dist = map_to_heavy(sequence, res_i, res_j, name_i, name_j, dist)

            out.append((res_i, name_i, res_j, name_j, dist))
        out_groups.append(out)
    return out_groups


def filter_groups(groups, remove_short=False, min_co=4):
    out = []
    for g in groups:
        keep = True
        for line in g:
            res_i, name_i, res_j, name_j, dist = line

            if res_i == 1 or res_j == 1:
                keep = False

            if remove_short:
                if abs(res_i - res_j) < min_co:
                    keep = False

        if keep:
            out.append(g)
    return out


def main():
    sequence = open('sequence.dat').readlines()[-1].strip()

    groups = fix_groups(get_groups(), sequence)
    groups = filter_groups(groups, remove_short=True, min_co=4)

    for g in groups:
        for line in g:
            print line[0], line[1], line[2], line[3], line[4]
        print


if __name__ == '__main__':
    main()

