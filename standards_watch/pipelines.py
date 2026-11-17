import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


class StatusSummaryPipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.count_status = Counter()

    def open_spider(self, spider):
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        self.count_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = self.results_dir / f'status_summary_{timestamp}.csv'
        with path.open('w', encoding='utf-8', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(sorted(self.count_status.items()))
            writer.writerow(['Total', sum(self.count_status.values())])
