import inspect

import scrapy

try:
    from standards_watch.items import StandardItem
except ModuleNotFoundError:
    raise AssertionError('Не найден файл `items.py`')
except ImportError as exc:
    raise AssertionError(f'Не найден класс `StandardItem` в файле {exc.name}')


def test_items_fields():
    assert inspect.isclass(StandardItem), (
        '`StandardItem` должен быть классом.'
    )
    assert issubclass(StandardItem, scrapy.Item), (
        '`StandardItem` должен наследоваться от `scrapy.Item`'
    )
    fields = ['identifier', 'name', 'status', 'url', 'published']
    for field in fields:
        assert field in list(StandardItem.fields.keys()), (
            f'В `StandardItem` не хватает атрибута `{field}`'
        )
