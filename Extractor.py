import os
import tarfile


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def extract_file(archive_path, extract_to):
    with tarfile.open(archive_path, 'r:gz') as tar:
        db_members = [tarinfo for tarinfo in tar.getmembers()
                      if tarinfo.name.startswith("./db/")]

        tar.extractall(extract_to, db_members)
        print(f'file {archive_path} extracted!')

    journal_files = [name for name in os.listdir(extract_to + 'db/') if name.endswith('.db-journal')]
    for journal_file in journal_files:
        db_file = os.path.splitext(journal_file)[0] + '.db'
        remove_file(extract_to + 'db/' + journal_file)
        remove_file(extract_to + 'db/' + db_file)

    pid_files = [name for name in os.listdir(extract_to + 'db/') if name.endswith('.pid')]
    for pid_file in pid_files:
        remove_file(extract_to + 'db/' + pid_file)


def extract_dir(path):
    archives = [name for name in os.listdir(path) if name.endswith('.tar.gz')]

    for archive in archives:
        extract_dir_name = os.path.splitext(os.path.splitext(archive)[0])[0]
        extract_file(path + archive, path + extract_dir_name + '/')
