def fixxpath(document):

    def __retokenisexpath__(tokens, prefix='x:'):
        for token in tokens:
            if token:
                yield prefix + token
            else:
                yield token

    def __wrappedxpath__(xpath):
        # Could do kwargs etc I dont care or need them
        tokens = xpath.split('/')
        nsmap = document.getroot().nsmap
        assert len(nsmap) <= 1
        assert None in nsmap
        new_nsmap = { 'x' : nsmap[None] }
        new_xpath = '/'.join(__retokenisexpath__(tokens))
        return document.xpath(new_xpath, namespaces=new_nsmap)
    return __wrappedxpath__
