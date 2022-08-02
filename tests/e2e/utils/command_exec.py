import os
from subprocess import PIPE, Popen
from utils.timeout import timeout
import time

KIALI_ACCOUNT_NAME = 'kiali-service-account'

class command_exec():

  def oc_apply(self, namespace):
    add_command_text = f"oc apply -n {namespace} -f {self}"
    stdout, stderr = Popen(add_command_text, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return "created" in stdout.decode() or "configure" in stdout.decode()

  def oc_delete(self, namespace):
    delete_command_text = f"oc delete -n {namespace} -f {self}"
    stdout, stderr = Popen(delete_command_text, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return "deleted" in stdout.decode()

  def oc_remove_cluster_role_rom_user_kiali(self):
    cmd = f'oc adm policy remove-cluster-role-from-user kiali system:serviceaccount:istio-system:{KIALI_ACCOUNT_NAME}'
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if 'cluster role \"kiali\" removed' in stdout.decode():
      return True
    print(
        f'Error remove-cluster-role-from-user for \"{KIALI_ACCOUNT_NAME}\": {stderr.decode()}'
    )
    return False

  def oc_add_cluster_role_to_user_kiali(self):
    cmd = f'oc adm policy add-cluster-role-to-user kiali system:serviceaccount:istio-system:{KIALI_ACCOUNT_NAME}'
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if 'cluster role \"kiali\" added'.format(KIALI_ACCOUNT_NAME) in stdout.decode():
      return True
    print(
        f'Error add-cluster-role-to-user for \"{KIALI_ACCOUNT_NAME}\": {stderr.decode()}'
    )
    return False

  def oc_get_kiali_configmap(self, file):
    cmd = f'oc get cm kiali -o yaml -n istio-system > {file}'
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return 'not found' not in stdout.decode() and len(stderr.decode()) == 0

  def oc_delete_kiali_config_map(self):
    cmd = 'oc delete cm kiali -n istio-system'
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return 'deleted' in stdout.decode() and 'Error' not in stderr.decode()

  def oc_create_kiali_config_map(self, file, remove_file = False):
    cmd = f'oc create -f {file} -n istio-system'
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if 'created' not in stdout.decode() or 'Error' in stderr.decode():
      print(f"{stderr.decode()}")
      return False

    if remove_file:
      cmd = f'rm -f {file}'
      Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()

    return True


  def oc_delete_kiali_pod(self):
    cmd = "oc delete pod -n istio-system `oc get pods -n istio-system | grep kiali | awk '{print $1;}'`"
    stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    return 'deleted' in stdout.decode() and 'Error' not in stderr.decode()

  def oc_wait_for_kiali_state(self, state):
    cmd = "oc get pods -n istio-system | grep kiali | awk '{print $3;}'"

    with timeout(seconds=120, error_message=f'Timed out waiting for Kiali state: {state}'):
      while True:
          stdout, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
          if state in stdout.decode():
              # Allow container time to init
              time.sleep(3)
              break

          time.sleep(2)

    return True
