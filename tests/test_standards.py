import inspect

import scrapy

try:
    from standards_watch.spiders.standards import StandardsSpider
except ModuleNotFoundError:
    raise AssertionError('Не найден файл `standards.py`')
except ImportError as exc:
    raise AssertionError(
        f'Не найден класс `{exc.args[0].split()[3]}` в файле {exc.name}',
    )


def test_standards_spider():
    assert inspect.isclass(StandardsSpider), (
        '`StandardsSpider` должен быть классом.'
    )
    assert issubclass(StandardsSpider, scrapy.Spider), (
        '`StandardsSpider` должен наследоваться от `scrapy.Spider`'
    )


def test_standards_spider_attrs():
    assert StandardsSpider.name, (
        'Класс `StandardsSpider` должен иметь атрибут `name`.'
    )
    assert StandardsSpider.name == 'standards', (
        'Значением атрибута `name` класса `StandardsSpider` лучше задать `pep`'
    )
    assert hasattr(StandardsSpider, 'start_urls'), (
        'Класс `StandardsSpider` должен иметь атрибут `start_urls`.'
    )
    assert StandardsSpider.start_urls == ['https://www.w3.org/TR/'], (
        'В классе StandardsSpider для атрибута start_urls установите список со значением '
        'https://www.w3.org/TR/'
    )


def test_standards_spider_parse():
    got = StandardsSpider()
    assert hasattr(got, 'parse'), (
        f'Класс `{got.__class__.__name__}` должен иметь метод `parse`.'
    )
    assert callable(got.parse), (
        f'Убедитесь, что `parse` в классе {got.__class__.__name__} '
        '- это вызываемый метод.'
    )

