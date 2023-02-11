from kubernetes import client, config
import kubernetes

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()

# Define the label and value to filter nodes by
label = "affinity"
value = "on-demand"

# Get all nodes with the specified label
nodes = v1.list_node(label_selector=f"{label}={value}")


# Initialize variables to store the sum of pods and sum of resource usage
sum_pods = 0
sum_cpu = 0
sum_memory = 0
affinity_pods = 0

for node in nodes.items:
    # Get all pods scheduled on the nodes
    pods = v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node.metadata.name}")
    affinity_pods = [pod for pod in pods.items if not pod.spec.affinity]
    sum_pods += len(affinity_pods)

    # Iterate through the pods and add the resource usage to the sum
    for pod in affinity_pods:
        for container in pod.spec.containers:
            try:
                sum_cpu += kubernetes.utils.parse_quantity(container.resources.requests["cpu"])
                sum_memory += kubernetes.utils.parse_quantity(container.resources.requests["memory"])
            except TypeError:
                continue


# Print the results
print(f"Number of pods without affinity: {sum_pods}")
print(f"Sum of resource usage (CPU): {sum_cpu}")
print(f"Sum of resource usage (memory): {sum_memory}")
