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


class Hipbone(SpackApplication):
    '''Define Hipbone application'''
    name = 'hipbone'

    maintainers('klinveam')

    tags('thermal hydraulics', 'transport', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('openblas', spack_spec='openblas')

    software_spec('hipbone',
                  spack_spec='hipbone +cuda',
                  compiler='gcc9')

    required_package('hipbone')

    workload('standard', executables=['execute'])

    workload_variable('mode', default='Serial', 
                      description='the mode to run OCCA in', 
                      workloads=['standard'])

    workload_variable('nx', default='24', 
                      description='the number of spectral elements in the x-direction per MPI rank', 
                      workloads=['standard'])

    workload_variable('ny', default='24', 
                      description='the number of spectral elements in the y-direction per MPI rank', 
                      workloads=['standard'])

    workload_variable('nz', default='24', 
                      description='the number of spectral elements in the z-direction per MPI rank', 
                      workloads=['standard'])

    workload_variable('p', default='14', 
                      description='the order of the polynomial used to approximate the solution', 
                      workloads=['standard'])    

    executable('execute', 'occa modes && hipBone -m {mode} -nx {nx} -ny {ny} -nz {nz} -p {p}', use_mpi=True)

    # hipBone: 14, 37595375, 421.9203, 100, 1.12e-05,  1.9,  2.3, 8.91e+06; N, DOFs, elapsed, iterations, time per DOF, avg BW (GB/s), avg GFLOPs, DOFs*iterations/ranks*time 
    # hipBone: NekBone FOM =  2.4 GFLOPs. 

    figure_of_merit('Solve Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'Major kernels total time \(seconds\): (?P<solve_time>.*)',
                    group_name='solve_time', units='s')
