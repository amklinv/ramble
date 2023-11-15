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


class Openmc(SpackApplication):
    '''Define OpenMC application'''
    name = 'openmc'

    maintainers('klinveam')

    tags('monte carlo', 'transport', 'benchmark')

    default_compiler('gcc9', spack_spec='gcc@9.3.0')

    software_spec('impi2018',
                  spack_spec='intel-mpi@2018.4.274')

    software_spec('openmc',
                  spack_spec='openmc +mpi +openmp +ipo',
                  compiler='gcc9')

    required_package('openmc')

    workload('standard', executables=['set-cross-sections','execute'], inputs=['benchmark', 'cross_sections'])

    # Get the benchmark repo
    input_file('benchmark',
               url='https://github.com/jtramm/openmc_offloading_benchmarks/archive/refs/heads/main.zip',
               description='HPC Benchmarking input for OpenMC')

    # Get the cross section library from https://openmc.org/official-data-libraries/
    # Version VIII.0 is missing C0, which causes a runtime error for all but the small and medium benchmarks
    # We want VII.1
    input_file('cross_sections',
               url='https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz',
               description='Cross section library input for OpenMC')

    # We have to use a relative path because of the fixed string length for the cross section file
    executable('set-cross-sections',
               template=["sed -i -e 's~<materials>~<materials>\\n<cross_sections>../../../../inputs/openmc/standard/cross_sections/cross_sections.xml</cross_sections>~g' -i {workload_input_dir}/benchmark/progression_tests/small/materials.xml"],
               use_mpi=False)

    executable('execute', 'openmc {workload_input_dir}/benchmark/progression_tests/small', use_mpi=True)

    figure_of_merit('Simulation Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'\s*Total time in simulation\s*=\s*(?P<solve_time>.*)',
                    group_name='solve_time', units='s')

    figure_of_merit('Inactive Batch Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'\s*Time in inactive batches\s*=\s*(?P<inactive_time>.*)',
                    group_name='inactive_time', units='s')

    figure_of_merit('Active Batch Time', log_file='{experiment_run_dir}/{experiment_name}.out',
                    fom_regex=r'\s*Time in active batches\s*=\s*(?P<active_time>.*)',
                    group_name='active_time', units='s')