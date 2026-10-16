"""scripts/tf_provided_codify.py: imported OCIDs become references, other
identifying values become variables, tags and nulls are dropped, the
resources are split by file, and nothing identifying reaches a committable
file."""
import pytest

from scripts import tf_provided_codify as cz

CPT = "ocid1.compartment.oc1..aaaacompartment"
VCN = "ocid1.vcn.oc1.iad.aaaavcn"
SUB = "ocid1.subnet.oc1.iad.aaaasubnet"
CL = "ocid1.cluster.oc1.iad.aaaacluster"
IMG = "ocid1.image.oc1.iad.aaaaimage"
# global addresses for the leak detector, built at run time so this file holds
# no address literal (tests/test_no_ip_addresses.py)
SRC = ".".join(["8", "8", "4", "4"]) + "/32"
OTHER = ".".join(["1", "1", "1", "1"]) + "/32"

IMPORTS = f'''import {{
  to = oci_core_vcn.vcn_main
  id = "{VCN}"
}}

import {{
  to = oci_core_subnet.subnet_workers
  id = "{SUB}"
}}

import {{
  to = oci_containerengine_cluster.cluster_oke
  id = "{CL}"
}}

import {{
  to = oci_core_network_security_group_security_rule.nsg_a_rule_00
  id = "networkSecurityGroups/ocid1.networksecuritygroup.oc1.iad.x/securityRules/ABC"
}}
'''

GEN = f'''# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "{VCN}"
resource "oci_core_vcn" "vcn_main" {{
  cidr_blocks    = ["10.0.0.0/16"]
  compartment_id = "{CPT}"
  defined_tags = {{
    "Oracle-Tags.CreatedBy" = "oracleidentitycloudservice/someone@example.com"
  }}
  freeform_tags  = {{}}
  display_name   = "oke-vcn"
  ipv6private_cidr_blocks = null
}}

resource "oci_core_subnet" "subnet_workers" {{
  cidr_block     = "10.0.1.0/24"
  compartment_id = "{CPT}"
  vcn_id         = "{VCN}"
  display_name   = "workers (private)"
}}

resource "oci_core_security_list" "sl_lb" {{
  compartment_id = "{CPT}"
  vcn_id         = "{VCN}"
  ingress_security_rules {{
    protocol = "6"
    source   = "{SRC}"
  }}
  egress_security_rules {{
    destination = "0.0.0.0/0"
    protocol    = "all"
  }}
}}

resource "oci_containerengine_cluster" "cluster_oke" {{
  compartment_id = "{CPT}"
  vcn_id         = "{VCN}"
  endpoint_config {{
    subnet_id = "{SUB}"
  }}
}}

resource "oci_containerengine_node_pool" "pool_oke_cpu" {{
  cluster_id     = "{CL}"
  compartment_id = "{CPT}"
  ssh_public_key = "ssh-rsa AAAAB3Nza someone"
  node_metadata = {{
    apiserver_host           = "192.0.2.3"
    oke-kubeproxy-proxy-mode = "iptables"
  }}
  node_config_details {{
    size = 2
    freeform_tags = {{
      "role" = "worker"
    }}
    placement_configs {{
      availability_domain = "Uocm:US-ASHBURN-AD-1"
      subnet_id           = "{SUB}"
    }}
  }}
  node_source_details {{
    image_id    = "{IMG}"
    source_type = "IMAGE"
  }}
}}
'''


@pytest.fixture
def out():
    c = cz.Codifier(cz.import_refs(IMPORTS))
    return c, cz.render(c, c.codify(GEN))


def test_import_refs_skip_path_ids():
    refs = cz.import_refs(IMPORTS)
    assert refs[VCN] == "oci_core_vcn.vcn_main.id"
    assert len(refs) == 3


def test_split_by_resource_type(out):
    _, files = out
    assert set(files) == {"network.tf", "cluster.tf", "nodepool.tf", "variables.tf",
                          "terraform.tfvars.example"}
    assert 'resource "oci_core_security_list" "sl_lb"' in files["network.tf"]
    assert "oci_containerengine_node_pool" in files["nodepool.tf"]
    assert "oci_containerengine_node_pool" not in files["cluster.tf"]


def test_imported_ocids_become_references(out):
    _, files = out
    assert "vcn_id         = oci_core_vcn.vcn_main.id" in files["cluster.tf"]
    assert "subnet_id = oci_core_subnet.subnet_workers.id" in files["cluster.tf"]
    assert "cluster_id     = oci_containerengine_cluster.cluster_oke.id" in files["nodepool.tf"]


def test_other_identifying_values_become_variables(out):
    c, files = out
    assert c.vars["compartment_ocid"]["value"] == CPT
    assert c.vars["pool_oke_cpu_image_id"]["value"] == IMG
    assert c.vars["availability_domain_1"]["value"] == "Uocm:US-ASHBURN-AD-1"
    assert c.vars["pool_oke_cpu_ssh_public_key"]["kind"] == "ssh"
    assert c.vars["sl_lb_source"]["value"] == SRC
    assert c.vars["pool_oke_cpu_apiserver_host"] == {
        "value": "192.0.2.3", "kind": "host", "res": "pool_oke_cpu", "key": "apiserver_host"}
    assert "apiserver_host           = var.pool_oke_cpu_apiserver_host" in files["nodepool.tf"]
    assert 'pool_oke_cpu_apiserver_host = "<oke-api-private-ip>"' in files["terraform.tfvars.example"]
    assert len(c.vars) == 6  # the compartment is one variable however often it appears
    assert 'variable "compartment_ocid"' in files["variables.tf"]
    assert 'variable "region"' in files["variables.tf"]


def test_private_and_open_cidrs_and_plain_strings_stay(out):
    _, files = out
    net = files["network.tf"]
    assert '"10.0.1.0/24"' in net and '"0.0.0.0/0"' in net and '"workers (private)"' in net


def test_tags_nulls_and_generator_comments_dropped(out):
    c, files = out
    text = "".join(files.values())
    assert "defined_tags" not in text and "freeform_tags" not in text
    assert "ipv6private_cidr_blocks" not in text and "__generated__" not in text
    assert "size = 2" in files["nodepool.tf"] and "placement_configs {" in files["nodepool.tf"]
    assert c.n_dropped == 4


def test_no_committable_file_leaks(out):
    _, files = out
    for name, text in files.items():
        assert cz.leaks(text) == [], name
    assert 'compartment_ocid = "ocid1.compartment.oc1..<compartment-ocid>"' in files["terraform.tfvars.example"]


def test_real_values_only_in_tfvars(out):
    c, _ = out
    real = cz.tfvars(c)
    assert real.startswith(cz.TFVARS_HEAD) and CPT in real and SRC in real


def test_leak_scan_catches_each_kind():
    assert cz.leaks(f'  x = "{CPT}"')
    assert cz.leaks('  # someone@example.com')
    assert cz.leaks('  ad = "Uocm:US-ASHBURN-AD-2"')
    assert cz.leaks(f'  source = "{OTHER}"')
    assert not cz.leaks('  source = "10.0.0.0/16"  # 0.0.0.0/0')


def test_unknown_resource_type_refused():
    with pytest.raises(ValueError):
        cz.Codifier({}).codify('resource "oci_identity_policy" "p" {\n  name = "x"\n}\n')


def test_controller_managed_list_ignores_only_its_rules():
    c = cz.Codifier(cz.import_refs(IMPORTS), {"sl_lb"})
    net = cz.render(c, c.codify(GEN))["network.tf"]
    sl = net[net.index('resource "oci_core_security_list" "sl_lb"'):]
    assert "ignore_changes = [ingress_security_rules, egress_security_rules]" in sl
    assert "Kubernetes owns" in sl
    assert net.count("lifecycle {") == 1


def test_controller_managed_refuses_unknown_or_wrong_type():
    with pytest.raises(ValueError, match="no such resource"):
        cz.Codifier({}, {"sl_typo"}).codify(GEN)
    with pytest.raises(ValueError, match="not a security list"):
        cz.Codifier({}, {"subnet_workers"}).codify(GEN)


def test_foreign_tfvars_carried_over_and_conflicts_refused(out):
    c, _ = out
    real = cz.tfvars(c, 'region = "us-ashburn-1"\n# note\ncompartment_ocid = "' + CPT + '"\n')
    assert real.count("compartment_ocid") == 1
    assert 'region = "us-ashburn-1"' in real and "carried over" in real
    with pytest.raises(ValueError, match="compartment_ocid"):
        cz.tfvars(c, 'compartment_ocid = "ocid1.compartment.oc1..other"\n')
    assert "carried over" not in cz.tfvars(c, cz.tfvars(c))


def test_controller_managed_comment_says_whether_rules_are_written():
    empty = 'resource "oci_core_security_list" "sl_e" {\n  display_name = "e"\n}\n'
    out = "".join(cz.Codifier({}, {"sl_e"}).codify(empty)["network.tf"])
    assert "It held no rules" in out and "rules above" not in out
    out = "".join(cz.Codifier({}, {"sl_lb"}).codify(GEN)["network.tf"])
    assert "The rules above are the" in out


def _cloud_init_b64():
    import base64
    import gzip
    text = '"ssh_authorized_keys":\n- "ssh-ed25519 AAAAC3NzaC1 someone@example.com"\n'
    return base64.b64encode(gzip.compress(text.encode())).decode()


def test_user_data_becomes_a_variable():
    blob = _cloud_init_b64()
    src = ('resource "oci_containerengine_node_pool" "pool_a" {\n  node_metadata = {\n'
           f'    user_data = "{blob}"\n  }}\n}}\n')
    c = cz.Codifier({})
    files = cz.render(c, c.codify(src))
    assert "user_data = var.pool_a_user_data" in files["nodepool.tf"]
    assert c.vars["pool_a_user_data"]["kind"] == "userdata"
    assert 'pool_a_user_data = "<base64 gzip cloud-init>"' in files["terraform.tfvars.example"]
    assert all(cz.leaks(t) == [] for t in files.values())


def test_leak_scan_decodes_base64_and_gzip():
    hits = cz.leaks(f'    user_data = "{_cloud_init_b64()}"')
    assert "1: encoded email" in hits and "1: encoded SSH key" in hits
    assert cz.leaks('  key = "ssh-rsa AAAAB3Nza x"') == ["1: SSH key"]


def test_private_host_addresses_leak_subnets_do_not():
    assert cz.leaks('    apiserver_host = "192.0.2.3"')
    assert cz.leaks('  source = "192.0.2.4/32"')
    assert not cz.leaks('  cidr_block = "10.140.0.0/16"')
    assert not cz.leaks('  destination = "0.0.0.0/0"')
