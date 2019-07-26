import os
import re
import codecs

class IgnoreFile():
    """Ignore file Class"""
    
    def __init__(self, ignore_file):
        """Processes ignore files and applying the pattern specified on

        * a list of strings (`filter`),
        * recursively on all files and subfolders (`walk`) or
        * merely on a text strings (`is_not_ignored`)

        Parameters
        ----------
        ignore_file : str, optional
            path to text file

        """

        self._reg_exp = []
        try:
            with codecs.open(ignore_file, encoding="utf-8") as fl:
                for line in fl:
                    line = line.strip().replace(".", "\.")
                    if not line.startswith("#") and len(line) > 0:
                        self._reg_exp.append( "^" + line.replace("*", ".*"))

        except:
            raise RuntimeError("Can't read ignore file: {0}".format(
                ignore_file))


    def is_not_ignored(self, text):
        """False if the text matches on of the pattern specified in the
        ignore file

        """

        for reg in self._reg_exp:
            if re.match(reg, text) is not None:
                    # print("* ignored: " + txt)
                    return False
        return True


    def filter(self, array):
        """filter array according the pattern specified in the ignore-file
        """

        return filter(self.is_not_ignored, array)

    def walk(self, path):
        """generator functions to walk recursively through all files in a
        subdirectory, while ignoring the files specified in the ignore_file

        """

        # TODO: no checked on windows

        path = os.path.abspath(path)
        for dirpath, _, files in os.walk(path):
            subfolder_name = dirpath.replace(path, "")[1:] + os.path.sep
            if self.is_not_ignored(subfolder_name):
                for filename in self.filter(files):
                    yield os.path.join(dirpath, filename)

