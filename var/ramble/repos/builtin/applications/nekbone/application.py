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


class Nekbone(SpackApplication):
    '''Define Nekbone application'''
    name = 'nekbone'

    maintainers('klinveam')

    tags('thermal hydraulics', 'transport', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('nekbone',
                  spack_spec='nekbone +mpi',
                  compiler='gcc9')

    required_package('nekbone')

    workload('standard', executables=['gather-data', 'copy-input','set-nprocs','build','execute'])

    executable('gather-data', 'which gfortran', use_mpi=False)

    executable('copy-input', 'cp {in_files} {experiment_run_dir}', use_mpi=False)

    executable('set-nprocs',
               template=["sed -i -e 's/      parameter (lp = .*)                      ! max number of processors/      parameter (lp = {n_ranks})                      ! max number of processors/g' -i SIZE"],
               use_mpi=False)

    workload_variable('in_files', default='{nekbone}/bin/Nekbone/test/nek_mgrid/{SIZE,data.rea}',
                      description='Input files for results',
                      workloads=['standard'])

    workload_variable('n_ranks', default='1',
                      description='Number of MPI processes',
                      workloads=['standard'])

    executable('build', 'makenek', use_mpi=False)

    executable('execute', './nekbone', use_mpi=True)

    figure_of_merit('Solve Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'\s*Solve Time\s*=\s*(?P<solve_time>.*)',
                    group_name='solve_time', units='s')