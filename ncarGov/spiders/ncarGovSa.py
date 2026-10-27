import json

import scrapy


class NcargovsaSpider(scrapy.Spider):
    """Collect document metadata from the Saudi National Center for Archives
    (ncar.gov.sa) public search API.

    Usage:
        scrapy crawl ncarGovSa -O output.json
        scrapy crawl ncarGovSa -a pages=5 -O sample.json
    """

    name = 'ncarGovSa'
    allowed_domains = ['ncar.gov.sa']
    api_url = 'https://ncar.gov.sa/api/ApiDocument/GetAllDocuments/'
    default_pages = 396

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'AUTOTHROTTLE_ENABLED': True,
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://ncar.gov.sa/Documents/AdvancedSearch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    search_filter = {
        "Name": "", "Number": "", "ApprovDateFrom": "", "ApprovDateTo": "",
        "PublishDate": None, "ApprovTypeId": None, "PrintYear": None, "PrintNo": "",
        "OmAlQourahId": None, "IsTemporaryHidden": None, "IsValid": None, "Status": None,
        "ReleasOrgId": None, "IsPrinted": False, "IsTranslated": False,
        "GeneralList": [], "ParticularList": [], "GovernmentList": [], "TopicalList": [],
        "ChildGovernmentList": [], "alphabeticalTopicId": None, "GovernmentalAgencyId": None,
        "alphabeticalCategoryId": None, "AlphabeticCategoryList": [], "tags": "",
        "documnetTypeId": None, "Type": 1, "sortDescending": True,
    }

    def __init__(self, pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = int(pages) if pages else self.default_pages

    def start_requests(self):
        for page in range(self.pages):
            yield scrapy.FormRequest(
                url=self.api_url,
                formdata={
                    'Filter': json.dumps(self.search_filter),
                    'pageNumber': str(page),
                },
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        data = json.loads(response.text)
        for listing in data.get('Collection', []):
            approvals = listing.get('DocumentApprovals') or [{}]
            yield {
                'Id': listing.get('Id'),
                'NameAR': listing.get('NameAR'),
                'SummeryAR': listing.get('SummeryAR'),
                'OriginalAttachPath': listing.get('OriginalAttachPath'),
                'Tags': listing.get('Tags'),
                'ApproveDateHigri': approvals[0].get('ApproveDateHigri'),
                'ApproveTool': listing.get('ApproveTool'),
            }
