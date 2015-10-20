"""script for digesting profiling output
to profile functions, wrap them into decorator @profile('file_name.prof')

source: http://code.djangoproject.com/wiki/ProfilingDjango
"""

import sys

try:
    from pstats import Stats
    stats = Stats()
except ImportError:
    from hotshot import stats

_stats = stats.load(sys.argv[1])
# _stats.strip_dirs()
_stats.sort_stats('time', 'calls')
_stats.print_stats(20)
