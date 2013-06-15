from lucene import initVM, System, NIOFSDirectory, File
from lucene import IndexWriter, Document, Field
from lucene import IndexSearcher, StandardAnalyzer, Version
import threading

class TestThread(threading.Thread):

    def __init__(self, vm):
        threading.Thread.__init__(self)
        self.vm = vm

    def run(self):
        self.vm.attachCurrentThread()
        
        indexDir = NIOFSDirectory(File("/tmp/test-index"))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        searcher = IndexSearcher(indexDir)

if __name__ == '__main__':
    threads = []

    vm = initVM()

    # Make a fake index for the test
    indexDir = NIOFSDirectory(File("/tmp/test-index"))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    writer   = IndexWriter(indexDir, analyzer, True, IndexWriter.MaxFieldLength(256))

    doc = Document()
    doc.add(Field('test', 'Test data', Field.Store.YES, Field.Index.ANALYZED))
    writer.addDocument(doc)
    writer.close()

    for i in xrange(256):
        t = TestThread(vm)
        threads.append(t)
        t.setDaemon(True)
        t.start()

    for thread in threads:
        thread.join()
