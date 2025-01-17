from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check

class ApiServerKubeletClientCertAndKey(BaseK8Check):
    def __init__(self):
        id = "CKV_K8S_72"
        name = "Ensure that the --kubelet-client-certificate and --kubelet-client-key arguments are set as appropriate"
        categories = [CheckCategories.KUBERNETES]
        supported_entities = ['containers']
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_entities)

    def get_resource_id(self, conf):
        return f'{conf["parent"]} - {conf["name"]}' if conf.get('name') else conf["parent"]

    def scan_spec_conf(self, conf):
        if conf.get("command") is not None:
            if "kube-apiserver" in conf["command"]:
                hasCertCommand = False
                hasKeyCommand = False
                for command in conf["command"]:
                    if command.startswith("--kubelet-client-certificate"):
                        hasCertCommand = True
                    elif command.startswith("--kubelet-client-key"):
                        hasKeyCommand = True
                return CheckResult.PASSED if hasCertCommand and hasKeyCommand else CheckResult.FAILED
           
        return CheckResult.PASSED

check = ApiServerKubeletClientCertAndKey()