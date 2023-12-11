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


class Laghos(SpackApplication):
    '''Define Laghos application'''
    name = 'laghos'

    maintainers('klinveam')

    tags('thermal hydraulics', 'transport', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('laghos',
                  spack_spec='laghos',
                  compiler='gcc9')

    required_package('laghos')

    workload('standard', executables=['execute'])

    workload_variable('dimension', default='3',
                      description='Dimension of the problem',
                      workloads=['standard'])

    workload_variable('mesh', default='default',
                      description='Mesh file to use',
                      workloads=['standard'])

    workload_variable('rs', default='2',
                      description='Number of times to refine the mesh uniformly in serial',
                      workloads=['standard'])

    workload_variable('rp', default='0',
                      description='Number of times to refine the mesh uniformly in parallel',
                      workloads=['standard'])

    executable('execute', 'laghos -dim {dimension} -m {mesh} -rs {rs} -rp {rp}', use_mpi=True)

    figure_of_merit('Solve Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'Major kernels total time \(seconds\): (?P<solve_time>.*)',
                    group_name='solve_time', units='s')
