from kubernetes import client, config

# Load Kubernetes config
config.load_kube_config()

# Create a Namespace API client
v1 = client.CoreV1Api()
networkingV1 = client.NetworkingV1Api()

# Get all namespaces with the label "istio-injection: enabled"
# namespaces = v1.list_namespace(label_selector='istio-injection=enabled')
namespaces = v1.list_namespace()

for ns in namespaces.items:
    
    # Get all services in the namespace
    services = v1.list_namespaced_service(ns.metadata.name)
    for svc in services.items:
        
        try:
            if not svc.metadata.annotations:
                svc.metadata.annotations = {}
            
            # Annotate the service with ingress.kubernetes.io/service-upstream="true"
            # and networking.istio.io/exportTo=".zone-traffic"
            svc.metadata.annotations.update({
                "service.kubernetes.io/topology-aware-hints": "auto",
            })
            v1.patch_namespaced_service(
                svc.metadata.name, ns.metadata.name, svc)
            
            print(f"Annotated service {svc.metadata.name} in namespace {ns.metadata.name}")
        except Exception as e:
            print(f"SKIPPING service {svc.metadata.name} in namespace {ns.metadata.name}")
            continue
    
    # Get all ingress objects in the namespace
    # ingresses = networkingV1.list_namespaced_ingress(ns.metadata.name)
    # for ing in ingresses.items:
    #
    #     if not ing.metadata.annotations:
    #         ing.metadata.annotations = {}
    #
    #     # Annotate the ingress with konghq.com/preserve-host="false"
    #     ing.metadata.annotations.update({
    #         "konghq.com/preserve-host": "false"
    #     })
    #     networkingV1.patch_namespaced_ingress(
    #         ing.metadata.name, ns.metadata.name, ing)
    #
    #     print(f"Annotated ingress {ing.metadata.name} in namespace {ns.metadata.name}")
