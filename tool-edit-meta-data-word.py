import sys, zipfile
import shutil, re, os



useHelp = ('''Usage: : 
    python3 tool-edit-meta-data-word.py [options] [-in in-file] [-out out-file] 
or
    python3 tool-edit-meta-data-word.py [-t time] [-c create] [-l lastcreate] [-in in-file] [-out out-file] 
    python3 tool-edit-meta-data-word.py -t 1000 -c 'nama-saya' -l 'nama-saya' [-in in-file] [-out out-file] 
Options:
    -h          help
    -in         input name file.
    -out        output name file.
    -t          total time (int), dalam satuan menit, ex : 10, 20, 400, 2000, dll.
    -c          create (string), nama yang membuat file word
    -l          last modified by (string), nama yang terakhir edit file''')

def argument():
    if (len(sys.argv) <= 2):
        print(useHelp)
        exit()
    
    totalTime, creator, lastModifiedBy, inputFile, outputFile = '', '', '', '', ''
    for i, ar in enumerate(sys.argv):
        if (ar == '-h'): 
            print(useHelp)
            exit()

        if (ar == '-t'): totalTime = sys.argv[i+1]
        if (ar == '-c'): creator = sys.argv[i+1]
        if (ar == '-l'): lastModifiedBy = sys.argv[i+1]
        if (ar == '-in'): inputFile = sys.argv[i+1]
        if (ar == '-out'): outputFile = sys.argv[i+1]

        if(totalTime == '') : totalTime = False
        if(creator == '') : creator = False
        if(lastModifiedBy == '') : lastModifiedBy = False
        if(inputFile == '') : inputFile = False
        if(outputFile == '') : outputFile = False
    return totalTime, creator, lastModifiedBy, inputFile, outputFile
        

def change_n_extract(oldName, newName, totalTime, creator, lastModifiedBy):
    shutil.copyfile(oldName, newName+'.zip')
    with zipfile.ZipFile(newName+'.zip', 'r') as zip_ref:
        zip_ref.extractall(f'./output')
    os.remove(newName+'.zip')
    
    #######################
    # Mengubah total time #
    #######################
    if (totalTime):
        f = open('output/docProps/app.xml', 'r').read()
        newTotalTime = f'<TotalTime>{totalTime}</TotalTime>'
        oldTotalTime = re.findall(r'<TotalTime>\d*</TotalTime>', f)[0]
        f = f.replace(oldTotalTime, newTotalTime)
        open('output/docProps/app.xml', 'w').write(f)
    
    #####################################
    # Mengubah creator & lastModifiedBy #
    #####################################
    f = open('output/docProps/core.xml', 'r').read()
    if (creator):
        newCreator = f'<dc:creator>{creator}</dc:creator>'
        oldCreator = re.findall(r'<dc:creator>.*?</dc:creator>', f)[0]
        f = f.replace(oldCreator, newCreator)
    
    if (lastModifiedBy):
        newLastModifiedBy = f'<cp:lastModifiedBy>{lastModifiedBy}</cp:lastModifiedBy>'
        oldLastModifiedBy = re.findall(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', f)[0]
        f = f.replace(oldLastModifiedBy, newLastModifiedBy)

    open('output/docProps/core.xml', 'w').write(f)

def compress_zip(odlName):
    from os.path import basename
    inputFiles = []
    zf = zipfile.ZipFile(odlName, 'w', compression=zipfile.ZIP_DEFLATED)
    for path, subdirs, files in os.walk('output/'):
        for name in files:
            nameFiles = os.path.join(path, name)
            zf.write(nameFiles, nameFiles.replace('output/', ''))


def main():
    totalTime, creator, lastModifiedBy, inputFile, outputFile = argument()
    change_n_extract(inputFile, outputFile, totalTime, creator, lastModifiedBy)
    compress_zip(outputFile)
    shutil.rmtree('output')
    print('Membuat duplikat berhasil ...')

if __name__ == "__main__":
    main()