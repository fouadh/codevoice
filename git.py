import subprocess
from pathlib import Path
import datetime
import csv

METADATA_SEPARATOR = '|'
FILE_INFO_SEPARATOR = '\t'


def git_log_to_csv(repo_path, output_csv, start_date=None):
  if start_date is None:
    start_date = default_start_date()

  files = get_repo_files(repo_path)

  output_path = Path(output_csv)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  with open(output_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['commit', 'author', 'date', 'file', 'added', 'removed'])
    for file in files:
      log = retrieve_git_log(repo_path, start_date, file)
      process_log(log, writer)


def process_log(log, writer):
  current_commit, current_author, current_date = None, None, None
  for line in log:
    if is_line_empty(line):
      continue
    elif is_line_with_date_info(line):
      current_commit, current_author, current_date = process_metadata_line(line)
    elif is_line_with_file_info(line):
      added, removed, file = process_file_line(line)
      if added is not None:
        writer.writerow([current_commit, current_author, current_date, file, added, removed])


def process_metadata_line(line):
  # Line format:  SHA-1|author|date
  parts = split_line(line, METADATA_SEPARATOR)
  current_commit = parts[0]
  current_author = parts[1]
  current_date = datetime.datetime.fromisoformat(parts[2])
  return current_commit, current_author, current_date.isoformat()


def process_file_line(line):
  # Line format:  added lines\tremoved lines\tfile path
  try:
    parts = split_line(line, FILE_INFO_SEPARATOR)
    added = int(parts[0])
    removed = int(parts[1])
    file = parts[2]
    return added, removed, file
  except ValueError:
    return None, None, None  # Skip binary files


def split_line(line, separator):
  return line.strip().split(separator)


def is_line_with_file_info(line):
  return (FILE_INFO_SEPARATOR in line
          and len(split_line(line, FILE_INFO_SEPARATOR)) == 3)


def is_line_with_date_info(line):
  return (METADATA_SEPARATOR in line
          and FILE_INFO_SEPARATOR not in line
          and len(split_line(line, METADATA_SEPARATOR)) == 3)


def is_line_empty(line):
  return not line.strip()


def default_start_date():
  one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
  return datetime.datetime.fromisoformat(one_year_ago.isoformat()).isoformat()


def retrieve_git_log(repo_path, start_date, file_path):
  cmd = ['git', 'log', '--follow', '--pretty=format:%H|%an|%ad', '--numstat', '--date=iso', '--after=' + start_date,
         '--', file_path]
  result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, text=True)
  return result.stdout.strip().split('\n')


def get_repo_files(repo_path: Path):
  result = subprocess.run(['git', 'ls-files'], cwd=repo_path, stdout=subprocess.PIPE, text=True)
  return result.stdout.strip().split('\n')
