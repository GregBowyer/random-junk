import fnmatch, sys, os, re, zipfile, time, string
import readzip
import pprint

master_jar_list={}
master_class_list={}
dup_jar_list={}
dup_class_list={}

class DictionaryHolder:
    pass

def listFiles(root, patterns='*', recurse=1, return_folders=0):
    pattern_list = patterns.split(';')  
    
    class Bunch:
        def __init__(self, **kwds): self.__dict__.update(kwds)
    
    arg = Bunch(recurse=recurse, pattern_list=pattern_list, return_folders=return_folders, results=[])
    
    def visit(arg, dirname, files):
        for name in files:
            fullname = os.path.normpath(os.path.join(dirname, name))
            if arg.return_folders or os.path.isfile(fullname):
                for pattern in arg.pattern_list:
                    if fnmatch.fnmatch(name, pattern):
                        arg.results.append(fullname)
                        addToAudit(fullname)
                        break
            if not arg.recurse: files[:]=[]
    
    os.path.walk(root, visit, arg)  
        
    return arg.results

def addToAudit(full_jarname):
    y, m, d, h, min, sec, a,b,c = time.localtime(os.path.getmtime(full_jarname))
    time_modified = m.__str__() + "/" + d.__str__() + "/" + y.__str__()
    jarbase = os.path.split(full_jarname)[0]
    jarfile = os.path.split(full_jarname)[1]
    
    if(master_jar_list.has_key(jarfile)):
        dup_jar_list[(full_jarname, jarfile)] = master_jar_list[jarfile]
    else:
        master_jar_list[jarfile] = (full_jarname, time_modified)
    
    readZip(full_jarname, jarfile)
    return

def readZip(full_filename, jar_name_only):
    class_name_pattern=re.compile("/?\w*.class$")
    z=zipfile.ZipFile(full_filename, "r")
        
    for aFile in z.filelist:
        if class_name_pattern.search(aFile.filename):
            split_class_elements = aFile.filename.split('/')
            class_name = split_class_elements[-1]
            package_name = string.join(split_class_elements[:-1], "/")
            
            modified_date = y,m,d,h,min,s = aFile.date_time 
            formatted_modified_date = m.__str__() + '/' + d.__str__() + '/' + y.__str__()
            lookup_key = (class_name, package_name)  

            file_locations = []
            if(master_class_list.has_key(class_name)):
                full_jarname, mod_date = master_jar_list[jar_name_only]
                if(dup_class_list.has_key(lookup_key)):
                    file_locations = dup_class_list[lookup_key][2]
                    file_locations.append(full_filename)
                    dup_class_list[lookup_key] = (full_jarname, formatted_modified_date, file_locations)
                else:
                    file_locations.append(master_class_list[class_name][0])
                    dup_class_list[lookup_key] = (full_jarname, formatted_modified_date, file_locations)
            else:
                master_class_list[class_name] = (full_filename, package_name, formatted_modified_date)
    return

def report():
    """Dumps the jars """
    o=DictionaryHolder()

    o.master_jar_list=master_jar_list
    o.master_class_list=master_class_list
    o.dup_jar_list=dup_jar_list
    o.dup_class_list=dup_class_list

    pp = pprint.PrettyPrinter()
    pp.pprint(master_jar_list)
    pp.pprint(dup_jar_list)
    pp.pprint(dup_class_list)

    return

def main(root, pattern):
    thefiles = listFiles(root, pattern)
    report()

#The __main__ method is the internal representation of a stand alone scripts execution
if __name__ == '__main__':
    #There is something buggy about the way Jython picks up this second argument.  This works fine in Python and I didn't
    #want to use the getopts module without dire need.  The second arg was appearing as jython.jar and I took the easy way
    #out to get the pattern that I wanted - *.jar
    main(sys.argv[1], sys.argv[2] )  
else:
    print "listFiles loaded as module"
