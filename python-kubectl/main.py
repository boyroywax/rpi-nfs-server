from kubernetes import client, config
from pprint import pprint

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config(config_file='/Users/jdev/Documents/GitHub/rpi-nfs/k3s-ansible/files/k3s.yml')


def pod_ip():
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (
            i.status.pod_ip, i.metadata.namespace,
            i.metadata.name
            )
        )


def api_support():
    print("Supported APIs (* is preferred version):")
    print("%-20s %s" % ("core", ",".join(client.CoreApi().get_api_versions().versions)))
    for api in client.ApisApi().get_api_versions().groups:
        versions = []
        for v in api.versions:
            name = ""
            if v.version == api.preferred_version.version and len(
                    api.versions) > 1:
                name += "*"
            name += v.version
            versions.append(name)
        print("%-40s %s" % (api.name, ",".join(versions)))


def label_master():
    """
    Label the k3s King and taint them
    """
    master_host = "k3s-gateway"
    api_instance = client.CoreV1Api()

    body = {
        "metadata": {
            "labels": {
                "kubernetes.io/role": "master"
            }
        }
    }

    body2 = {
        "metadata": {
            "labels": {
                "node-role.kubernetes.io/master": ""
            }
        }
    }

    api_response = api_instance.patch_node(master_host, body)

    pprint(api_response)

    api_response = api_instance.patch_node(master_host, body2)

    pprint(api_response)

    api_response = client.models.v1_taint.V1Taint(master_host, effect="NoSchedule")

    pprint(api_response)


def label_nodes():
    """
    Label the nodes for work
    """

    api_instance = client.CoreV1Api()

    node_body = {
        "metadata": {
            "labels": {
                "kubernetes.io/role": "node"
            }
        }
    }

    node_body2 = {
        "metadata": {
            "labels": {
                "node-role.kubernetes.io/node": ""
            }
        }
    }

    nodes = [
        "nfs1", "nfs2", "k3s-worker-01", "k3s-worker-02", "k3s-worker-03",
        "k3s-worker-04", "k3s-master"
    ]

    for node in nodes:
        api_response = api_instance.patch_node(node, node_body)

        pprint(api_response)

        api_response = api_instance.patch_node(node, node_body2)

        pprint(api_response)


pod_ip()
label_master()