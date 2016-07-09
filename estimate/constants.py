# global constants
GLOBAL_SAMPLE_PERCENT = 2

NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
PAPI, ITIMER = "emptyPapiHandler", "emptyItimerHandler"
PAPI_OVERHEAD_PERCENT, ITIMER_OVERHEAD_PERCENT = "papiOvPercent", "itimerOvPercent"
PERCENT, UNW_PERCENT, INSTR_PERCENT, SAMPLE_PERCENT = "percent", "unwPercent", "instrPercent", "samplePercent"
DRIVER_SEC, DRIVER_PERCENT = "driverSeconds", "driverPercent"
AVERAGE_WITH_DII, AVERAGE_WITHOUT_DII = "average-14", "mean-13"

OUT_DIR = "out-estimate"

PN_DEPRECATED = {
    'InstrumentAll': 'ss-all',
    'Instrument': 'ss-cpd',
    'MinInstrHeuristic': 'ss-min',
    'ConjInstrHeuristic': 'ss-conj',
    'LibUnwStandard': 'unw-all',
    'LibUnwUnique': 'unw-min',
    'UnwStaticLeaf': 'hybrid-st',
    'UnwindSample': 'hybrid-dyn',

    'OvCompensation': '',
    'RemoveUnrelated': '',
    'SanityCheck': '',
    'Reset': ''
}

PN = {
    'ss-all': 'ss-all',
    'ss-cpd': 'ss-cpd',
    'ss-min': 'ss-min',
    'ss-conj': 'ss-conj',
    'unw-all': 'unw-all',
    'unw-min': 'unw-min',
    'hybrid-st': 'hybrid-st',
    'hybrid-dyn': 'hybrid-dyn',

    'OvCompensation': '',
    'RemoveUnrelated': '',
    'SanityCheck': '',
    'Reset': ''
}

PHASE_ORDER_INTERNAL = ['InstrumentAll', 'Instrument', 'MinInstrHeuristic', 'ConjInstrHeuristic',
               'LibUnwStandard', 'LibUnwUnique', 'UnwStaticLeaf', 'UnwindSample']

# COL = {
#     'ss-all': 'violet',
#     'ss-cpd': 'blue',
#     'ss-min': 'purple',
#     'ss-conj': 'cyan',
#     'unw-all': 'red',
#     'unw-min': 'pink',
#     'hybrid-dyn': 'green',
#     'hybrid-st': 'yellow'
# }

COL = {
    'hybrid-st':    "#1B9E77",
    'ss-conj':      "#D95F02",
    'unw-all':      "#7570B3",
    'unw-min':      "#E7298A",
    'hybrid-dyn':   "#66A61E",
    'ss-min':       "#E6AB02",
    'ss-cpd':       "#A6761D",
    'ss-all':       "#666666"
}

DRIVER_PHASES = ["ss-cpd", "ss-min", "unw-all", "unw-min", "hybrid-st", "hybrid-dyn"]

PHASE_ORDER = []
for name in PHASE_ORDER_INTERNAL:
    PHASE_ORDER.append(PN_DEPRECATED[name])