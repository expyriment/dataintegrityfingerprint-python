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

        self.ignore_file = ignore_file

    @property
    def ignore_file(self):
        return self._ignore_file

    @ignore_file.setter
    def ignore_file(self, flname):
        self._reg_exp = []
        self._ignore_file = os.path.abspath(flname)
        try:
            with codecs.open(self._ignore_file, encoding="utf-8") as fl:
                for line in fl:
                    line = line.strip()
                    if not line.startswith("#") and len(line) > 0:
                        self._reg_exp.append( "^" +
                                line.replace(".", "\.").replace("*", ".*"))

        except:
            raise RuntimeError("Can't read ignore file: {0}".format(self._ignore_file))

    def is_not_ignored(self, text):
        """False if the text matches one of the pattern specified in the
        ignore file

        """

        for reg in self._reg_exp:
            if re.match(reg, text) is not None:
                    # print("* ignored: " + text)
                    return False
        return True


    def filter(self, array):
        """filter array according the pattern specified in the ignore-file
        """

        return filter(self.is_not_ignored, array)

    def walk(self, path, ignore_youself=False):
        """generator function to walk recursively through all files in a
        subdirectory, while ignoring the files specified in the ignore_file

        Parameters
        -----------
        ignore_youself : bool
            if true the ignorefile will not be included in the returned file
            list (default: False)

        """
        # TODO: not checked on windows

        path = os.path.abspath(path)
        for dirpath, _, files in os.walk(path):
            subfolder_name = os.path.relpath(dirpath, start=path) + os.path.sep
            # filter folder
            if self.is_not_ignored(subfolder_name):
                # filter filenames
                for filename in self.filter(files):
                    #  filter join folder/filenames
                    if self.is_not_ignored(os.path.join(subfolder_name,
                                                        filename)):
                        fl = os.path.join(dirpath, filename)
                        # exclude yourself
                        if not ignore_youself or fl != self.ignore_file:
                            yield fl
