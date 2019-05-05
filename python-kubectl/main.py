from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

# Configs can be set in Configuration class directly or using helper utility

KUBE_CONFIG='/Users/jdev/Documents/GitHub/rpi-nfs/k3s-ansible/files/k3s.yml'
MASTER_NODE = "k3s-gateway"
WORKER_NODES = [
    "nfs1", "nfs2", "k3s-worker-01", "k3s-worker-02", "k3s-worker-03",
    "k3s-worker-04", "k3s-master"
]


def load_kube():
    kubernetes.config.load_kube_config(config_file=KUBE_CONFIG)
    api_instance = kubernetes.client.AdmissionregistrationApi()

    try:
        api_response = api_instance.get_api_group()
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling AdmissionregistrationApi->get_api_group: %s\n" % e)

    try:
        api_instance = kubernetes.client.CoreV1Api()
        # pprint(api_instance.get_api_resources())
    except ApiException as e:
        return print("Exception when creating api_instance CoreV1Api->get_api_group: %s\n" % e)
    
    return api_instance


# def pod_ip():
#     v1 = client.CoreV1Api()
#     print("Listing pods with their IPs:")
#     ret = v1.list_pod_for_all_namespaces(watch=False)
#     for i in ret.items:
#         print("%s\t%s\t%s" % (
#             i.status.pod_ip, i.metadata.namespace,
#             i.metadata.name
#             )
#         )


# def api_support():
#     print("Supported APIs (* is preferred version):")
#     print("%-20s %s" % ("core", ",".join(client.CoreApi().get_api_versions().versions)))
#     for api in client.ApisApi().get_api_versions().groups:
#         versions = []
#         for v in api.versions:
#             name = ""
#             if v.version == api.preferred_version.version and len(
#                     api.versions) > 1:
#                 name += "*"
#             name += v.version
#             versions.append(name)
#         print("%-40s %s" % (api.name, ",".join(versions)))


def label_master(api, master=MASTER_NODE):
    """
    Label the k3s King and taint them
    """


    # body = {
    #     "metadata": {
    #         "labels": {
    #             "kubernetes.io/role": "master"
    #         }
    #     }
    # }

    # body2 = {
    #     "metadata": {
    #         "labels": {
    #             "node-role.kubernetes.io/master": ""
    #         }
    #     }
    # }

    taint = {
        "spec": {
            "taints": {
                "effect": "NoSchedule",
                "key": "node-role.kubernetes.io/master",
                "value": "NoSchedule"
                }
            }
        }
        
    # api_response = api.patch_node(master, body)

    # pprint(api_response)

    # api_response = api.patch_node(master, body2)

    # pprint(api_response)

    api_response = api.patch_node(master, taint)

    pprint(api_response)

    # api_response = client.models.v1_taint.V1Taint(master, effect="NoSchedule")


def label_nodes(api, nodes=WORKER_NODES):
    """
    Label the nodes for work
    """

    api_instance = api

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

    for node in nodes:
        api_response = api_instance.patch_node(node, node_body)

        pprint(api_response)

        api_response = api_instance.patch_node(node, node_body2)

        pprint(api_response)


def main():
    api = load_kube()
    # label_master(api)
    label_nodes(api)


if __name__ == "__main__":
    main()