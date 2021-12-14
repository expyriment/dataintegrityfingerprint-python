import filecmp
import glob
import io
import os
import shutil
import tempfile
import unittest
import urllib.request
import zipfile

from dataintegrityfingerprint import DataIntegrityFingerprint


def setUpModule():
    print("Downloading example data...")
    global TMP_DIR
    global EXAMPLE_DATA_PATH
    TMP_DIR = tempfile.mkdtemp()
    http_response = urllib.request.urlopen("https://github.com/expyriment/dataintegrityfingerprint/archive/refs/heads/master.zip")
    z = zipfile.ZipFile(io.BytesIO(http_response.read()))
    z.extractall(path=TMP_DIR)
    EXAMPLE_DATA_PATH = os.path.join(TMP_DIR,
                                     "dataintegrityfingerprint-master",
                                     "example_data")

def tearDownModule():
    global TMP_DIR
    shutil.rmtree(TMP_DIR)


class AllAlgorithmsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print(f"\nSetting up '{__name__}.{__class__.__name__}'...")
        available_algorithms = \
            DataIntegrityFingerprint.CRYPTOGRAPHIC_ALGORITHMS \
            + DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS
        self.difs = []
        global TMP_DIR
        global EXAMPLE_DATA_PATH
        for data in glob.glob(f"{EXAMPLE_DATA_PATH}/*/"):
            for algorithm in available_algorithms:
                for multiprocessing in (False, True):
                    dif = DataIntegrityFingerprint(
                        data, hash_algorithm=algorithm,
            multiprocessing=multiprocessing,
                        allow_non_cryptographic_algorithms=True)
                    dif.generate()
                    self.difs.append(dif)
        self.tmp_filenames = []
        print("Running tests...")

    def test_calculate_dif(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                extension = "".join(
                    x for x in dif.hash_algorithm.lower() if x.isalnum())
                checksums_file = glob.glob(
                    f"{dif.data}-*.{extension}")[0]
                correct_dif = os.path.splitext(
                    os.path.split(checksums_file)[1])[0].split("-")[-1]
                self.assertEqual(dif.dif, correct_dif)

    def test_save_checksums(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                tmp_file, tmp_filename = tempfile.mkstemp()
                os.close(tmp_file)
                dif.save_checksums(tmp_filename)
                self.tmp_filenames.append(tmp_filename)
                extension = "".join(
                    x for x in dif._hash_algorithm.lower() if x.isalnum())
                checksums_file = glob.glob(
                    f"{dif.data}-*.{extension}")[0]
                self.assertTrue(filecmp.cmp(tmp_filename, checksums_file))

    def test_diff_checksums(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                extension = "".join(
                    x for x in dif.hash_algorithm.lower() if x.isalnum())
                checksums_file = glob.glob(
                    f"{dif.data}-*.{extension}")[0]
                self.assertEqual(dif.diff_checksums(checksums_file), "")

    @classmethod
    def tearDownClass(self):
        for tmp_filename in self.tmp_filenames:
            os.remove(tmp_filename)


class AllAlgorithmsFromChecksumsFileTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print(f"\nSetting up '{__name__}.{__class__.__name__}'...")
        available_algorithms = \
            DataIntegrityFingerprint.CRYPTOGRAPHIC_ALGORITHMS \
            + DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS
        self.difs = []
        global TMP_DIR
        global EXAMPLE_DATA_PATH
        for data in glob.glob(f"{EXAMPLE_DATA_PATH}/*/"):
            for algorithm in available_algorithms:
                for multiprocessing in (False, True):
                    extension = "".join(
                        x for x in algorithm.lower() if x.isalnum())
                    checksums_file = glob.glob(
                        f"{os.path.split(data)[0]}-*.{extension}")[0]
                    dif = DataIntegrityFingerprint(
                        checksums_file, from_checksums_file=True,
                        hash_algorithm=algorithm,
                        multiprocessing=multiprocessing,
                        allow_non_cryptographic_algorithms=True)
                    dif.generate()
                    self.difs.append(dif)
        self.tmp_filenames = []
        print("Running tests...")

    def test_calculate_dif(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                extension = "".join(
                    x for x in dif.hash_algorithm.lower() if x.isalnum())
                correct_dif = os.path.splitext(
                    os.path.split(dif.data)[1])[0].split("-")[-1]
                self.assertEqual(dif.dif, correct_dif)

    def test_save_checksums(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                tmp_file, tmp_filename = tempfile.mkstemp()
                os.close(tmp_file)
                dif.save_checksums(tmp_filename)
                self.tmp_filenames.append(tmp_filename)
                extension = "".join(
                    x for x in dif._hash_algorithm.lower() if x.isalnum())
                self.assertTrue(filecmp.cmp(tmp_filename, dif.data))

    def test_diff_checksums(self):
        for dif in self.difs:
            with self.subTest(data=dif.data, algorithm=dif.hash_algorithm):
                extension = "".join(
                    x for x in dif.hash_algorithm.lower() if x.isalnum())
                self.assertEqual(dif.diff_checksums(dif.data), "")

    @classmethod
    def tearDownClass(self):
        for tmp_filename in self.tmp_filenames:
            os.remove(tmp_filename)
