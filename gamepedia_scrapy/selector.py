class Selector:
    def __init__(p):
        self.p = p
    def text():
        return self.p.css('::text').extract_first()

    def attr(_attr):
        return self.p.css('::attr(%s)'%_attr).extract_first()

    def href():
        return self.attr('href')
