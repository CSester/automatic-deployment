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

  clonedRepositories.append((repository, commit, cloneFolder))

  return cloneFolder

def getDependencies():
  with lcd('deploy'):
    currentPwd = local('pwd', capture=True)
    with open(path.join(currentPwd, 'deploy.json')) as deployConfFile:
      deployConf = json.load(deployConfFile)

  return deployConf['dependencies']

def main(configPath):
  with open(configPath) as envFile:
    envData = json.load(envFile)
    for key, val in envData.items():
      env[key] = val

  local('mkdir -p ' + env.tmpFolder)
  with lcd(env.tmpFolder):
    recursiveClone(env["source-repository"], env["source-commit"])
    print("Checking canRun functions...")
    for repo in reversed(clonedRepositories):
      try:
        with lcd(path.join(repo[2], 'deploy')):
          sys.path.append(local('pwd', capture=True))
          import deploy
          if 'canRun' not in dir(deploy):
            print("No function canRun for deploy script in {}!".format(repo[0]))
          else:
            print("Function canRun exist for deploy script in {}!".format(repo[0]))
            try:
              ret_value = deploy.canRun()
            except Exception as e:
              print(e)
              ret_value = False
            if ret_value:
              print("Deploy can run!")
            else:
              raise EnvironmentError("Can not continue, missing requirements for deploy script in {}! Aborting...".format(repo[0]))
          sys.path.remove(local('pwd', capture=True))
      except ImportError as e:
        print("No module deploy for {}!".format(repo[0]))
        pass
      except EnvironmentError as e:
        local('rm -rf ../{}'.format(env.tmpFolder))
        raise
      finally:
        del sys.modules['deploy']
    print("Check done!")
    print("Running deploy functions...")
    for repo in reversed(clonedRepositories):
      try:
        with lcd(repo[2]):
          with lcd('deploy'):
            sys.path.append(local('pwd', capture=True))
            from deploy import runDeploy
            sys.path.remove(local('pwd', capture=True))
            env['source-repository'] = repo[0]
            env['source-commit'] = repo[1]
            execute(runDeploy)
      except Exception as e:
        print(e)
        pass
      finally:
        del sys.modules['deploy']
        local('rm -rf ' + repo[2])
    print("Run done!")
