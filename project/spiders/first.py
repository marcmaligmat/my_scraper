import scrapy
from scrapy_splash import SplashRequest
from scrapy.utils.python import to_unicode

class FirstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains = ['iscc-system.org']
    

    def start_requests(self):
        url = 'https://www.iscc-system.org/certificates/all-certificates'
       
        yield SplashRequest(
                url, 
                callback=self.parse,
               
                args={
                'wait': 1,
                'lua_source': self.script
                },
            )

    def parse(self, response):
        
        table_rows = response.xpath("//tbody/tr")
        # print(table_rows)
        # print(response.body)
        for table_row in table_rows:
            yield{
                'certificate' : table_row.xpath(".//td[1]/text()").get()
            }

        yield SplashRequest(
                url='https://www.iscc-system.org/certificates/all-certificates', 
                callback=self.parse,
                dont_filter=True,
                args={
                'wait': 1,
                'lua_source': self.script
                },
            )
            
    # def parse_item(self,response):
    #     table_rows = response.xpath("//tbody/tr")
    #     # print(table_rows)
    #     # print(response.body)
    #     for table_row in table_rows:
    #         yield{
    #             'certificate' : table_row.xpath(".//td[1]/text()").get()
    #         }
       

    script = """
        function main(splash, args)
            splash:on_request(function(request)
                request:set_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36')  	
            end)
            assert(splash:go(args.url))
            assert(splash:wait(1))

            assert(splash:wait(1))
            splash:set_viewport_full()
            nextbutton = splash:select("a[class='paginate_button next']")
            assert(nextbutton.mouse_click())
            assert(splash:wait(4))
            
                return {
                html = splash:html(),
                png = splash:png(),
                
            }
        end
    """
