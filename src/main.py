import json
from fabric.api import lcd, local, env, execute
from os import path
import sys

clonedRepositories = []

cloneIndex = 1

def recursiveClone(repository, commit):
  clonedFolderName = clone(repository, commit)

  with lcd(clonedFolderName):
    dependencies = getDependencies()

  for dependency in dependencies:
    recursiveClone(dependency['repository'], dependency['commit'])

def clone(repository, commit):
  if repository in clonedRepositories:
    raise 'Circular dependency'

  global cloneIndex
  cloneFolder = 'repo' + str(cloneIndex)
  cloneIndex += 1

  local('git clone ' + repository + ' -b ' + commit + ' ' + cloneFolder)

  clonedRepositories.append((repository, cloneFolder))

  return cloneFolder

def getDependencies():
  with lcd('deploy'):
    currentPwd = local('pwd', capture=True)
    with open(path.join(currentPwd, 'deploy.json')) as deployConfFile:
      deployConf = json.load(deployConfFile)

  return deployConf['dependencies']

def main():
  local('mkdir -p ' + env.tmpFolder)
  with lcd(env.tmpFolder):
    recursiveClone(env["source-repository"], env["source-commit"])
    for repo in reversed(clonedRepositories):
      try:
        with lcd(repo[1]):
          with lcd('deploy'):
            sys.path.append(local('pwd', capture=True))
            from deploy import runDeploy
            sys.path.remove(local('pwd', capture=True))
            execute(runDeploy)
      except Exception as e:
        print(e)
        pass
      finally:
        del sys.modules['deploy']
        local('rm -rf ' + repo[1])
