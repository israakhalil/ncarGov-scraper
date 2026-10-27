# ncarGov — Saudi National Archives Scraper | زاحف وثائق المركز الوطني للوثائق والمحفوظات

> Scrapy spider that paginates the public search API of [ncar.gov.sa](https://ncar.gov.sa) and exports document metadata.
> زاحف Scrapy يقرأ واجهة البحث العامة لبوابة المركز الوطني للوثائق والمحفوظات (السعودية) ويستخرج بيانات الوثائق عبر أكثر من 390 صفحة.

## Fields / الحقول

| Field | Description |
|---|---|
| `Id` | Document id |
| `NameAR` | Arabic title / العنوان |
| `SummeryAR` | Arabic summary / الملخص |
| `OriginalAttachPath` | Path of the original attachment |
| `Tags` | Tags |
| `ApproveDateHigri` | Hijri approval date / تاريخ الاعتماد الهجري |
| `ApproveTool` | Approval instrument |

A small sample of the output is in [`samples/ncarGovSa.sample.json`](samples/ncarGovSa.sample.json) (from an earlier run; it contains a few extra fields).

## Tech stack

Python · Scrapy · scrapy-xlsx (Excel export) · JSON POST pagination

## Usage / التشغيل

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# quick test: first 5 pages
scrapy crawl ncarGovSa -a pages=5 -O sample.json

# full crawl (396 pages) to JSON or Excel
scrapy crawl ncarGovSa -O output.json
scrapy crawl ncarGovSa -O output.xlsx
```

## Responsible use / الاستخدام المسؤول

- `ROBOTSTXT_OBEY` is enabled, with a 1 s download delay and AutoThrottle.
- The data comes from a public API; respect the site's terms of use and do not overload it.

## License

MIT
