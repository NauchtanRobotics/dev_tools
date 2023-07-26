import win32api
from pathlib import Path


def compare(folder_1: Path, folder_2: Path):
    """
    To compare the files and dll version numbers of two different directories, simply edit
    the function test_compare() near the bottom of this module, and the run

    python compare_dll_files.py

    You may need to put in the full path to python.exe, wherever that may be.

    """
    drivers_1 = {path.name for path in folder_1.iterdir() if path.suffix != ".pdb"}
    drivers_2 = {path.name for path in folder_2.iterdir() if path.suffix != ".pdb"}
    print("No. dll files found in folder 1: ", len(drivers_1))
    print("No. dll files found in folder 2: ", len(drivers_2))

    missing = list(drivers_2 - drivers_1)
    if len(missing) == 0:
        print("\nThere are none missing")
    else:
        print("Missing from David's")
    for item in sorted(missing):
        print(item)

    extra = list(drivers_1 - drivers_2)
    if len(extra) == 0:
        print("\nThere are no extras")
    else:
        print("\n\nExtras in David's")
    for item in sorted(extra):
        print(item)

    dll_file_paths_1 = [path for path in folder_1.iterdir() if path.suffix == ".dll"]
    dll_file_paths_2 = [path for path in folder_2.iterdir() if path.suffix == ".dll"]
    print("File version metadata for files in David's folder: ")
    file_versions_david = {get_version(file_path) for file_path in dll_file_paths_1}
    file_versions_brian = {get_version(file_path) for file_path in dll_file_paths_2}
    missing_versions = list(file_versions_brian - file_versions_david)
    print("\n\nMissing versions from David:")
    for file_version in missing_versions:
        print(file_version)

    extra_versions = list(file_versions_david - file_versions_brian)
    print("\n\nExtra versions from David:")
    for file_version in extra_versions:
        print(file_version)

# ver_strings=('Comments','InternalName','ProductName',
#     'CompanyName','LegalCopyright','ProductVersion',
#     'FileDescription','LegalTrademarks','PrivateBuild',
#     'FileVersion','OriginalFilename','SpecialBuild')
ver_string = 'FileVersion'


def get_version(fpath: Path):
    # fname = os.environ["comspec"]
    fname = fpath.name
    try:
        d = win32api.GetFileVersionInfo(str(fpath), '\\')
    except:
        return fname + "_unknown_version"

    # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
    # for n, v in d.items():
    #     print(n, v)

    pairs = win32api.GetFileVersionInfo(str(fpath), '\\VarFileInfo\\Translation')
    # \VarFileInfo\Translation returns list of available (language, codepage) pairs that can be used to
    # retrieve string info
    # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle two are language/codepage
    # pair returned from above
    file_n_vers = ""
    for lang, codepage in pairs:
        #print('lang: ', lang, 'codepage:', codepage)
        str_info = u'\\StringFileInfo\\%04X%04X\\%s' %(lang, codepage, ver_string)
        ## print str_info
        file_n_vers = fname + repr(win32api.GetFileVersionInfo(str(fpath), str_info))

    return file_n_vers


def test_compare():
    installed_path = Path("C:\\Shepherd Services\\Virtual RACAS 6")
    debug_path = Path(r"C:\VR_Software_Suite\virtual_racas_npws\virtual-racas\bin\Debug")
    compare(installed_path, debug_path)


if __name__ == "main":
    test_compare()

