from pathlib import Path


def compare_subfolder_names(root_1: Path, root_2: Path):
    sub_folders_1 = [pth.name for pth in root_1.iterdir()]
    sub_folders_2 = [pth.name for pth in root_2.iterdir()]
    diff_1 = set(sub_folders_1) - set(sub_folders_2)
    diff_2 = set(sub_folders_2) - set(sub_folders_1)
    aggregated = set(sub_folders_1 + sub_folders_2)
    num_additional = len(diff_1)
    if num_additional > 0:
        print("\nNumber of additional folder =" + str(num_additional))
        print("Extra folders include:\n" + "\n".join(diff_1))
    assert len(diff_2) == 0


def test_compare_subfolder_names():
    root_1 = Path("C:\\Scenic_Rim_2023")
    root_2 = Path("C:\\2023 Datasources\\Scenic_Rim_2023_Nov")
    compare_subfolder_names(root_1, root_2)
