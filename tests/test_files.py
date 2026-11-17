import csv
from pathlib import Path


def test_saved_live_exports_have_consistent_totals():
    results = Path(__file__).resolve().parents[1] / 'results'
    with next(results.glob('standards_*.csv')).open(encoding='utf-8', newline='') as source:
        documents = list(csv.DictReader(source))
    with next(results.glob('status_summary_*.csv')).open(encoding='utf-8', newline='') as source:
        summary = dict(list(csv.reader(source))[1:])
    assert documents
    assert int(summary.pop('Total')) == len(documents)
    assert sum(map(int, summary.values())) == len(documents)
