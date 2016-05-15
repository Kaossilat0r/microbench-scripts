# global constants
NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
PERCENT, UNW_PERCENT, INSTR_PERCENT = "percent", "unwPercent", "instrPercent"

OUT_DIR = "out-estimate"

PN = {
    'InstrumentAll': 'ss-all',
    'Instrument': 'ss-cpd',
    'MinInstrHeuristic': 'ss-min',
    'ConjInstrHeuristic': 'ss-conj',
    'LibUnwStandard': 'unw-all',
    'LibUnwUnique': 'unw-min',
    'UnwStaticLeaf': 'hybrid-static',
    'UnwindSample': 'hybrid',

    'OvCompensation': '',
    'RemoveUnrelated': '',
    'SanityCheck': '',
    'Reset': ''
}

PHASE_ORDER = ['InstrumentAll', 'Instrument', 'MinInstrHeuristic', 'ConjInstrHeuristic',
               'LibUnwStandard', 'LibUnwUnique', 'UnwStaticLeaf', 'UnwindSample']

PHASE_ORDER_DISPLAY = []
for name in PHASE_ORDER:
    PHASE_ORDER_DISPLAY.append(PN[name])
