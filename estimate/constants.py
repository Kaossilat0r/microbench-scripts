# global constants
NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
PERCENT, UNW_PERCENT, INSTR_PERCENT = "percent", "unwPercent", "instrPercent"

OUT_DIR = "out-estimate"

PHASE_ORDER = ['InstrumentAll', 'Instrument', 'MinInstrHeuristic', 'ConjInstrHeuristic',
               'LibUnwStandard', 'LibUnwUnique', 'UnwStaticLeaf', 'UnwindSample']

PN = {
    'InstrumentAll': 'ss-all',
    'Instrument': 'ss-cpd',
    'MinInstrHeuristic': 'ss-min',
    'ConjInstrHeuristic': 'ss-conj',
    'LibUnwStandard': 'unw-all',
    'LibUnwUnique': 'unw-min',
    'UnwStaticLeaf': 'hybrid-static',
    'UnwindSample': 'hybrid'
}
