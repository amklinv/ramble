# Copyright 2022-2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

import os
from ramble.appkit import *
from ramble.expander import Expander


class Quicksilver(SpackApplication):
    '''Define Quicksilver application'''
    name = 'quicksilver'

    maintainers('klinveam')

    tags('thermal hydraulics', 'transport', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('quicksilver',
                  spack_spec='quicksilver +openmp +mpi',
                  compiler='gcc9')

    required_package('quicksilver')

    workload('standard', executables=['execute'])

    workload_variable('in_file', default='{quicksilver}/Examples/CTS2_Benchmark/CTS2.inp',
                      description='Input file for results',
                      workloads=['standard'])

    workload_variable('nParticles', default='655360', description='Number of particles', workloads=['standard'])

    workload_variable('nx', default='64', description='Number of mesh elements in x', workloads=['standard'])
    workload_variable('ny', default='32', description='Number of mesh elements in y', workloads=['standard'])
    workload_variable('nz', default='32', description='Number of mesh elements in z', workloads=['standard'])

    workload_variable('lx', default='64', description='x-size of simulation (cm)', workloads=['standard'])
    workload_variable('ly', default='32', description='y-size of simulation (cm)', workloads=['standard'])
    workload_variable('lz', default='32', description='z-size of simulation (cm)', workloads=['standard'])

    workload_variable('xDom', default='4', description='Number of MPI ranks in x', workloads=['standard'])
    workload_variable('yDom', default='2', description='Number of MPI ranks in y', workloads=['standard'])
    workload_variable('zDom', default='2', description='Number of MPI ranks in z', workloads=['standard'])

    executable('execute', 'qs -i {in_file} --lx {lx} --ly {ly} --lz {lz} --nx {nx} --ny {ny} --nz {nz} --xDom {xDom} --yDom {yDom} --zDom {zDom} --nParticles {nParticles}', use_mpi=True)

    figure_of_merit('Figure of Merit', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'Figure Of Merit\s*(?P<fom>.*) \[Num Segments / Cycle Tracking Time\]',
                    group_name='fom', units='Segments / Cycle Tracking Time')