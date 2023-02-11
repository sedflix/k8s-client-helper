import json
from multiprocessing import Pool
from kubernetes import client, config
import re

# Set the string to search for
# search_strings = ["vault.token", "token.vault" "vault_token", "token_vault", "tokenvault", "vaulttoken"]
search_strings = ["\'kinesis_region\': \'ap-south-1\'"]


def is_present_in_string(string):
    string = str(string).lower()
    for search_string in search_strings:
        if string.find(search_string) != -1:
            return True
    return False


def check_configmap(configmap):
    # Extract the configmap name
    namesapce = configmap.metadata.namespace
    name = configmap.metadata.name
    
    if configmap.data is not None:
        # Search for the string in the configmap data
        if is_present_in_string(configmap.data):
            print(f"{namesapce} - {name}")


def check_deployment(deployment):
    # Extract the deployment name
    namespace = deployment.metadata.namespace
    name = deployment.metadata.name
    
    for container in deployment.spec.template.spec.containers:
        if container.env is not None:
            for env_var in container.env:
                if env_var.value is not None:
                    if is_present_in_string(env_var.value):
                        print(f"{namespace} - {name}")
                if env_var.name is not None:
                    if is_present_in_string(env_var.name):
                        print(f"{namespace} - {name}")


if __name__ == "__main__":
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    
    v1_apps = client.AppsV1Api()
    v1_core = client.CoreV1Api()
    
    with Pool(12) as p:
        # print("Checking deployments")
        # deployments = v1_apps.list_deployment_for_all_namespaces().items
        # p.map(check_deployment, deployments)
        #
        # print("Checking statefulsets")
        # statefulsets = v1_apps.list_stateful_set_for_all_namespaces().items
        # p.map(check_deployment, statefulsets)
        #
        # print("Checking daemonsets")
        # daemonsets = v1_apps.list_daemon_set_for_all_namespaces().items
        # p.map(check_deployment, daemonsets)
        #
        print("Checking configmaps")
        configmaps = v1_core.list_config_map_for_all_namespaces().items
        print("Got all configmaps")
        p.map(check_configmap, configmaps)
