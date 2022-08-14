import lookml
import re
from github import Github
import yaml
import argparse

def audit_file_dimensions(path, chosen_views, old, new):
  for view in proj.file(path).views:
    if chosen_views is not None:
      audit_views = chosen_views.split(',')
      if view.name in audit_views:
        for search in view.search('sql', re.escape(old)):
          search.sql.value = search.sql.value.replace(old, new)
        proj.put(proj.file(path))
      else:
        pass
    else:
      print('Auditing all views in proj.')
      for search in view.search('sql', re.escape(old)):
        search.sql.value = search.sql.value.replace(old, new)
      proj.put(proj.file(path))

def recurse(directory, chosen_views, old, new):
  for content in directory:
    if content.type == 'file':
      if 'view.lkml' in content.path:
        audit_file_dimensions(content.path, chosen_views, old, new)
      else:
        pass
    else:
      recurse(repo.get_contents(f'/{content.path}'), chosen_views, old, new)

if __name__ == "__main__":
  with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

  repo_name = config['config']['repo']
  proj = lookml.Project(
        repo=repo_name,
        access_token=config['config']['access_token']
  )

  git = Github(config['config']['access_token'])
  repo = git.get_repo(repo_name)
  contents = repo.get_contents("")
  parser = argparse.ArgumentParser(
        description='Audit Fields for Specific View(s)')

  parser.add_argument('--views', '-v', type=str, required=False, help='Comma Separated list of views to audit')
  parser.add_argument('--old', '-o', type=str, required=True, help='Old SQL string to replace')
  parser.add_argument('--new', '-n', type=str, required=True, help='New SQL string to substitute')

  args = parser.parse_args()
  print(args)

  return_obj = {
    "status":"Success", 
    "message": 'Auditing specific views.' if args.views else 'Auditing all views in project.'
  }
  recurse(contents, args.views, args.old, args.new)
  # Hit Deploy URL to Update Looker
  proj.deploy()
  
  print(return_obj)
