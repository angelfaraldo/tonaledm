import csv
import os
import shutil
from datetime import datetime

from numpy import array as nparray

from .conversions import key_to_int


def make_unique_dir(parent, tag=''):
    """
    creates a sub-folder in the specified directory
    with some of the algorithm parameters.
    :type parent: str
    :type tag: str
    """
    now = str(datetime.now())
    now = now[:now.rfind('.')]
    now = now.replace(':', '')
    now = now.replace(' ', '')
    now = now.replace('-', '')
    temp_folder = "{0}/{1}-{2}".format(parent, now, tag)
    try:  # TODO remove parameter info and allow to write it from script as tags
        os.mkdir(temp_folder)
    except OSError:
        print("'{}' already exists.".format(temp_folder))
    return temp_folder


def merge_files(dir_with_files, new_filename):
    o = open(new_filename, 'w')
    e = os.listdir(dir_with_files)
    for item in e:
        if '.key' in item:
            f = open(dir_with_files + '/' + item, 'r')
            l = f.read()
            o.write(l + '\n')
            f.close()
    o.close()


def results_directory(out_dir):
    """
    creates a sub-folder in the specified directory
    with some of the algorithm parameters.
    :type out_dir: str
    """
    if not os.path.isdir(out_dir):
        print("CREATING DIRECTORY '{0}'.".format(out_dir))
        if not os.path.isabs(out_dir):
            raise IOError("Not a valid path name.")
        else:
            os.mkdir(out_dir)
    return out_dir


def features_from_csv(csv_file, start_col=0, end_col=1):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(map(float, row[start_col:end_col]))
    return nparray(saved_values)


def stringcell_from_csv(csv_file, col=27):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(row[col])
    return nparray(saved_values)


def keycell_from_csv(csv_file, col=27):
    saved_values = []
    csv_file = open(csv_file, 'r')
    csv_file = csv.reader(csv_file, skipinitialspace=True)
    for row in csv_file:
        saved_values.append(key_to_int(row[col]))
    return nparray(saved_values)



def move_items_by_estimation(condition, destination, estimations_folder, origin):
    estimations = os.listdir(estimations_folder)
    for item in estimations:
        if '.key' in item:
            e = open(estimations_folder + '/' + item)
            e = e.read()
            if condition in e:
                print('moving...{0} {1}'.format(item, e))
                shutil.move(origin + '/' + item[:-3] + 'wav',
                            destination)


def move_items_by_id(condition, destination, results, origin):
    results = open(results, 'r')
    len_line = 1
    while len_line > 0:
        r = results.readline()
        c = r[r.find('\t') + 1:r.rfind(' (')]
        try:
            c = float(c)
            if condition in r and c < 1:
                file_name = r[:r.rfind('.key')] + '.key'
                shutil.move(origin + '/' + file_name, destination)
        except ValueError:
            pass
        len_line = len(r)


def move_items(origin, destination):
    estimations = os.listdir(origin)
    for item in estimations:
        if '.key' in item:
            print(item)
            e = open(origin + '/' + item)
            e = e.readline()
            e = e.split('\t')
            print(e[0])
            print(e[1])
            if e[0] == e[1]:
                print('moving...', item, e)
                shutil.move(origin + '/' + item, destination)


def index_files(my_dir):
    """
    Given a directory, it replaces the containing filesystem with increasing numerical values.

    """
    dir_files = os.listdir(my_dir)
    file_count = 0
    for each_file in dir_files:
        if os.path.splitext(each_file)[1] == '.mid':
            int_name = "{:03d}.mid".format(file_count)
            os.rename(os.path.join(my_dir, each_file), os.path.join(my_dir, int_name))
            file_count += 1


def finder(filepath):
    """
    Show a file in the Mac OSX window system.

    """
    from appscript import app, mactypes
    app("Finder").reveal(mactypes.Alias(filepath).alias)


def folderfiles(folderpath, ext=None, recursive=False):
    """
    Returns a list of absolute paths with the filesystem in the specified folder.

    """
    if recursive:
        def _rlistdir(path):
            rlist = []
            for root, subdirs, files in os.walk(path):
                for f in files:
                    rlist.append(os.path.join(root, f))
            return rlist

        list_of_files = _rlistdir(folderpath)

    else:
        list_of_files = [os.path.join(folderpath, item) for item in os.listdir(folderpath)]

    my_files = []
    for myFile in list_of_files:
        if not ext:
            my_files.append(myFile)
        elif os.path.splitext(myFile)[1] == ext:
            my_files.append(myFile)
        else:
            pass

    if not my_files:
        # raise FileNotFoundError("Did not find any file with the given extension.") PYTHON3
        raise IOError("Did not find any file with the given extension.")
    else:
        return my_files