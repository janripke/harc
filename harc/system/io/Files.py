import os

class Files:
    @staticmethod
    def list(folder, excludes=[]):
        results = []
        files = os.listdir(folder)
        for file in files:
            if file not in excludes:
                if os.path.isfile(os.path.join(folder, file)):
                    results.append(os.path.join(folder, file))
                if os.path.isdir(os.path.join(folder, file)):
                    results.extend(Files.list(os.path.join(folder, file)))
        return results

    @staticmethod
    def mkdir(folder):
        os.path.exists(folder)