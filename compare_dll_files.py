import win32api
from pathlib import Path


def compare(working_folder: Path, broken_folder: Path):
    """
    To compare the files and dll version numbers of two different directories, simply edit
    the function test_compare() near the bottom of this module, and the run

    python compare_dll_files.py

    You may need to put in the full path to python.exe, wherever that may be.

    """
    drivers_in_working1 = {path.name for path in working_folder.iterdir() if path.suffix != ".pdb"}
    drivers_in_broken2 = {path.name for path in broken_folder.iterdir() if path.suffix != ".pdb"}
    print("No. dll files found in folder 1: ", len(drivers_in_working1))
    print("No. dll files found in folder 2: ", len(drivers_in_broken2))

    missing_in_broken2 = list(drivers_in_broken2 - drivers_in_working1)
    if len(missing_in_broken2) == 0:
        print("\nThere are no extra dlls in broken folder")
    else:
        print("Extra dlls in broken folder (second arg):")
    for item in sorted(missing_in_broken2):
        print(item)

    extras_in_working1 = list(drivers_in_working1 - drivers_in_broken2)
    if len(extras_in_working1) == 0:
        print("\nThere are no extra dll files in the working folder")
    else:
        print("\n\nExtras dll files found in the working (first arg)")
    for item in sorted(extras_in_working1):
        print(item)

    dll_files_in_working = [path for path in working_folder.iterdir() if path.suffix == ".dll"]
    dll_files_in_broken = [path for path in broken_folder.iterdir() if path.suffix == ".dll"]
    print("File version metadata for files in working folder (first arg): ")
    file_versions_in_working = {get_version(file_path) for file_path in dll_files_in_working}
    file_versions_in_broken = {get_version(file_path) for file_path in dll_files_in_broken}
    extra_versions_in_broken = list(file_versions_in_broken - file_versions_in_working)
    print("\n\nExtra versions in broken folder (second arg):")
    for file_version in extra_versions_in_broken:
        print(file_version)

    extra_versions_in_working = list(file_versions_in_working - file_versions_in_broken)
    print("\n\nExtra versions found in working folder (second arg):")
    for file_version in extra_versions_in_working:
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
    broken_folder = Path("C:\\Shepherd Services\\Virtual RACAS 6")
    # debug_path = Path(r"C:\VR_Software_Suite\virtual_racas_npws\virtual-racas\bin\Debug")
    working_folder = Path("C:\\Shepherd Services\\Virtual RACAS 6 - NPWS")
    compare(working_folder, broken_folder)


if __name__ == "main":
    test_compare()

