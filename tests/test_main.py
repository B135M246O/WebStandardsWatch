import csv
import os
import subprocess
import sys
from pathlib import Path

import pytest
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse

from standards_watch.pipelines import StatusSummaryPipeline
from standards_watch.spiders.standards import StandardsSpider

FIXTURE = Path(__file__).parent / 'fixtures' / 'w3c_catalog.html'


def test_catalog_extracts_names_statuses_and_shortnames():
    response = HtmlResponse('https://www.w3.org/TR/', body=FIXTURE.read_bytes(), encoding='utf-8')
    items = list(StandardsSpider().parse(response))
    assert [item['identifier'] for item in items] == ['autoplay-detection', 'css-color-4', 'css-color-3']
    assert [item['status'] for item in items] == ['Draft Standard', 'Candidate Standard', 'Standard']
    assert items[0]['published'] == '2026-11-16'
    assert items[1]['name'] == 'CSS Color Module Level 4'
    assert all(item['url'].startswith('https://www.w3.org/TR/') for item in items)


def test_empty_catalog_fails_instead_of_exporting_fake_data():
    response = HtmlResponse('https://www.w3.org/TR/', body=b'<html></html>')
    with pytest.raises(CloseSpider):
        list(StandardsSpider().parse(response))


def test_summary_counts_every_document_and_closes_file(tmp_path):
    pipeline = StatusSummaryPipeline()
    pipeline.results_dir = tmp_path
    pipeline.open_spider(None)
    for status in ['Standard', 'Draft Standard', 'Standard']:
        item = {'status': status}
        assert pipeline.process_item(item, None) is item
    pipeline.close_spider(None)
    with next(tmp_path.glob('status_summary_*.csv')).open(encoding='utf-8', newline='') as output:
        assert list(csv.reader(output)) == [
            ['Статус', 'Количество'], ['Draft Standard', '1'], ['Standard', '2'], ['Total', '3'],
        ]


def test_run_scrapy_exports_document_csv(tmp_path):
    script = '''from scrapy.crawler import CrawlerProcess
from standards_watch.spiders.standards import StandardsSpider
import standards_watch.pipelines as pipeline
from pathlib import Path
import sys
pipeline.BASE_DIR = Path(sys.argv[2])
process = CrawlerProcess(settings={
    'LOG_ENABLED': False,
    'ITEM_PIPELINES': {'standards_watch.pipelines.StatusSummaryPipeline': 300},
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEEDS': {str(Path(sys.argv[2]) / 'results/standards.csv'): {'format': 'csv', 'fields': ['identifier', 'name', 'status', 'url', 'published']}},
})
process.crawl(StandardsSpider, start_urls=[Path(sys.argv[1]).as_uri()])
process.start()
'''
    result = subprocess.run([sys.executable, '-c', script, str(FIXTURE.resolve()), str(tmp_path)],
                            capture_output=True, text=True, timeout=30, env=os.environ.copy())
    assert result.returncode == 0, result.stderr
    outputs = list((tmp_path / 'results').glob('*.csv'))
    assert len(outputs) == 2
    with (tmp_path / 'results' / 'standards.csv').open(encoding='utf-8', newline='') as output:
        rows = list(csv.DictReader(output))
    assert len(rows) == 3
    assert rows[2]['identifier'] == 'css-color-3'
