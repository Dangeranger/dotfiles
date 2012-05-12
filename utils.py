import os
import sys
import subprocess
import zipfile

def Prompt( prompt, options ):
    '''
    Prompts the user for input
    @param: prompt    Initial text for the prompt
    @param: options   A dict mapping options to functions
    @return:    Returns the same as the selected actionFunc
    '''
    entryToActionMap = []
    optionsList = []
    usedPrefixes = []
    for (text,func) in options.iteritems():
        entries = [ text ]
        if text[0] not in usedPrefixes:
            text = text[0] + '(%s)' % text[1:]
            entries.append( text[0] )
            usedPrefixes.append( text[0] )
        entryToActionMap.append( (entries,func) )
        optionsList.append( text )
    while True:
        action = raw_input( prompt + ', '.join( optionsList ) )
        for (entries,actionFunc) in entryToActionMap:
            if action in entries:
                return actionFunc()

def DoLink( orig, target ):
    '''
    Links a file in place, making a backup first
    @param: orig    The file to link from
    @param: target  The target path
    '''
    if os.path.exists( target ):
        os.rename( target, target + '.orig' )
    parentDir = os.path.dirname( target ) 
    if not os.path.exists( parentDir ):
        print "Making path %s" % parentDir
        os.makedirs( parentDir )
    print "Linking %s to %s" % ( orig, target )
    if 'symlink' in dir( os ):
        os.symlink( os.path.abspath( orig ), target )
    else:
        # Probably just python < 3.2 on windows.
        # Fall back on mklink
        subprocess.check_call( [ 
            'mklink', target, os.path.abspath( orig )
            ], shell=True )

def LinkFile( orig, target ):
    actualTarget = os.path.expanduser( target )
    shouldBackup = False
    if not os.path.exists( actualTarget ):
        DoLink( orig, actualTarget )
    else:
        if os.path.islink( actualTarget ):
            if( os.path.samefile( actualTarget, orig ) ):
            	print "%s is already symlinked in place." % orig
            	return
        print "%s already exists" % target
        def DoDiff():
            origFullPath = os.path.abspath( orig )
            subprocess.call(
                    [ 'diff', '-u', actualTarget, origFullPath ],
                    stdout = sys.stdout,
                    stderr = sys.stderr
                    )
        Prompt( 'Action? ', {
            'replace' : lambda: DoLink( orig, actualTarget ),
            'skip' : lambda: None,
            'quit' : quit,
            'diff' : DoDiff
            } )
    
def Unzip( filename, destPath ):
    if not os.path.exists( filename ):
        print "Unzip Error: File %s does not exist" % filename
    try:
        z = zipfile.ZipFile( filename )
        print "Extracting %s to %s" % ( filename, destPath )
        z.extractall( destPath )
        z.close()
    except:
        # Fall back on running unzip
        print "Attempting unzip via external tool"
        subprocess.check_call(
                [ 'unzip', filename, '-d', destPath ]
                )
    print "Done.  Deleting %s" % filename
    os.unlink( filename )

def GetGit( name, url, destPath ):
    '''
    Clones a git repo, or updates if already cloned
    @param: name        The name of the project
    @param: url         The url of the git repository
    @param: destPath    The destination folder for the repo
    '''
    if os.path.exists( destPath ):
        print "%s already installed.  Pulling from origin" % name
        cwd = os.getcwd()
        try:
            os.chdir( destPath )
            subprocess.check_call( 'git pull', shell=True )
        finally:
            os.chdir( cwd )
    else:
        print "Installing %s from remote repo" % name
        subprocess.check_call( 
                'git clone "%s" "%s"' % ( url, destPath ),
                shell=True
                )
