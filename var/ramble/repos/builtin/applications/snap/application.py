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


class Snap(SpackApplication):
    '''Define SNAP application'''
    name = 'snap'

    maintainers('klinveam')

    tags('benchmark-app', 'mini-app', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('snap',
                  spack_spec='hpcg@3.1 +mpi +openmp',
                  compiler='gcc9')

    required_package('snap')

    workload('standard', executables=['copy-input', 'set-nthreads', 'execute', 'copy-output'])

    executable('copy-input', 'cp {in_file} {experiment_run_dir}/input.txt', use_mpi=False)
    executable('set-nthreads',
               template=["sed -i -e 's/  nthreads=.*/  nthreads={n_threads}/g' -i input.txt",
                         "sed -i -e 's/  npey=.*/  npey={npey}/g' -i input.txt",
                         "sed -i -e 's/  npez=.*/  npez={npez}/g' -i input.txt"],
               use_mpi=False)
    executable('execute', 'gsnap input.txt output.txt', use_mpi=True)

    # The output file name seems to be truncated to 64 characters by SNAP
    # This gets around that limitation
    executable('copy-output', 'cp output.txt {out_file}', use_mpi=False)

    workload_variable('in_file', default='{snap}/qasnap/benchmark/inp',
                      description='Input file for results',
                      workloads=['standard'])

    workload_variable('out_file', default='{experiment_run_dir}/output',
                      description='Output file for results',
                      workloads=['standard'])

    workload_variable('npey', default='4',
                      description='Process grid y dimension',
                      workloads=['standard'])

    workload_variable('npez', default='4',
                      description='Process grid z dimension',
                      workloads=['standard'])

    figure_of_merit('Solve Time', log_file='{out_file}',
                    fom_regex=r'\s*Solve\s*(?P<exec_time>.*)',
                    group_name='exec_time', units='s')