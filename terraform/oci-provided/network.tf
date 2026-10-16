# The PROVIDED OKE cluster, codified via terraform import: plan only, NEVER
# apply (CLAUDE.md, the 2026-10-07 exception); every command through
# scripts/tf_provided.sh. Written by scripts/tf_provided_codify.py from the
# generated configuration: OCIDs are references or variables (values in the
# gitignored terraform.tfvars), tags and null attributes dropped.

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_11" {
  description               = "Allow ALL egress from workers to pods"
  destination               = oci_core_network_security_group.nsg_pods_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_02" {
  description               = "Allow TCP egress to OKE control plane from workers for health check"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10250
      min = 10250
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_04" {
  description               = "Allow TCP ingress to kube-apiserver from 0.0.0.0/0"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_05" {
  description               = "Allow ALL ingress to pods from Kubernetes control plane for webhooks served by pods"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_cp_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_13" {
  description               = "Allow TCP ingress to OKE control plane from worker nodes"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_workers_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 12250
      min = 12250
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_02" {
  description               = "Allow ALL egress from pods for cross-node pod communication when using NodePorts or hostNetwork: true"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_bastion_tbhcuw_rule_04" {
  description               = "Allow TCP egress from bastion to OCI services"
  destination               = "all-iad-services-in-oracle-services-network"
  destination_type          = "SERVICE_CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_06" {
  description               = "Allow ALL ingress to pods for cross-node pod communication when using NodePorts or hostNetwork: true"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_workers_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_security_list" "sl_pub_lb_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "pub_lb-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id

  # Kubernetes owns this list's rules: the OKE cloud controller adds and
  # removes them for the Streamlit LoadBalancer (security-list management
  # mode, k8s/overlays/oke-provided-public-ui). It held no rules at
  # import (2026-10-07), so none are written here; the plan does not compare them.
  lifecycle {
    ignore_changes = [ingress_security_rules, egress_security_rules]
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_01" {
  description               = "Allow SSH ingress to workers from bastion"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 22
      min = 22
    }
  }
}

resource "oci_core_subnet" "subnet_int_lb_tbhcuw" {
  cidr_block                 = "10.140.0.32/27"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "int_lb-tbhcuw"
  dns_label                  = "in"
  ipv4cidr_blocks            = ["10.140.0.32/27"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = true
  prohibit_public_ip_on_vnic = true
  route_table_id             = oci_core_route_table.rt_nat_route.id
  security_list_ids          = [oci_core_security_list.sl_int_lb_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_07" {
  description               = "Allow TCP egress from OKE control plane to OCI services"
  destination               = "all-iad-services-in-oracle-services-network"
  destination_type          = "SERVICE_CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_route_table" "rt_default_route_table_for_oke_test_vcn_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "Default Route Table for oke-test-vcn-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_security_list" "sl_default_security_list_for_oke_test_vcn_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "Default Security List for oke-test-vcn-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id

  # Kubernetes owns this list's rules: the OKE cloud controller adds and
  # removes them for the Streamlit LoadBalancer (security-list management
  # mode, k8s/overlays/oke-provided-public-ui). It held no rules at
  # import (2026-10-07), so none are written here; the plan does not compare them.
  lifecycle {
    ignore_changes = [ingress_security_rules, egress_security_rules]
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_int_lb_tbhcuw_rule_04" {
  description               = "Allow TCP egress from internal load balancers to workers for Node Ports"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_08" {
  description               = "Allow TCP egress from workers to OKE control plane"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 12250
      min = 12250
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_13" {
  description               = "Allow ALL egress from workers to other workers"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_12" {
  description               = "Allow TCP egress for Kubernetes control plane inter-communication"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group" "nsg_operator_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "operator-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_subnet" "subnet_operator_tbhcuw" {
  cidr_block                 = "10.140.0.16/29"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "operator-tbhcuw"
  dns_label                  = "op"
  ipv4cidr_blocks            = ["10.140.0.16/29"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = true
  prohibit_public_ip_on_vnic = true
  route_table_id             = oci_core_route_table.rt_nat_route.id
  security_list_ids          = [oci_core_security_list.sl_default_security_list_for_oke_test_vcn_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_00" {
  description               = "Allow TCP ingress to kube-apiserver from bastion host"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_operator_tbhcuw_rule_04" {
  description               = "Allow TCP egress from operator to OCI services"
  destination               = "all-iad-services-in-oracle-services-network"
  destination_type          = "SERVICE_CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_operator_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_subnet" "subnet_pods_tbhcuw" {
  cidr_block                 = "10.140.128.0/18"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "pods-tbhcuw"
  dns_label                  = "po"
  ipv4cidr_blocks            = ["10.140.128.0/18"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = true
  prohibit_public_ip_on_vnic = true
  route_table_id             = oci_core_route_table.rt_nat_route.id
  security_list_ids          = [oci_core_security_list.sl_default_security_list_for_oke_test_vcn_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_service_gateway" "sgw_service_gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "service-gateway"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  services {
    service_id = var.sgw_service_gateway_service_id
  }
}

resource "oci_core_vcn" "vcn_oke_test_vcn_tbhcuw" {
  cidr_block              = "10.140.0.0/16"
  cidr_blocks             = ["10.140.0.0/16"]
  compartment_id          = var.compartment_ocid
  display_name            = "oke-test-vcn-tbhcuw"
  dns_label               = "tbhcuw"
  ipv6private_cidr_blocks = []
  is_ipv6enabled          = false
  security_attributes     = {}
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_14" {
  description               = "Allow TCP egress from OKE control plane to Kubelet on worker nodes"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10250
      min = 10250
    }
  }
}

resource "oci_core_dhcp_options" "dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw" {
  compartment_id   = var.compartment_ocid
  display_name     = "Default DHCP Options for oke-test-vcn-tbhcuw"
  domain_name_type = "CUSTOM_DOMAIN"
  vcn_id           = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  options {
    custom_dns_servers  = []
    search_domain_names = [var.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw_search_domain_names]
    type                = "SearchDomain"
  }
  options {
    custom_dns_servers  = []
    search_domain_names = []
    server_type         = "VcnLocalPlusInternet"
    type                = "DomainNameServer"
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_bastion_tbhcuw_rule_03" {
  description               = "Allow SSH ingress to bastion from 0.0.0.0/0"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 22
      min = 22
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_10" {
  description               = "Allow TCP ingress to workers for health check from internal load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10256
      min = 10256
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_02" {
  description               = "Allow ICMP egress from public load balancers to worker nodes for path discovery"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(1)
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_04" {
  description               = "Allow ICMP egress from pods for path discovery"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = jsonencode(1)
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_05" {
  description               = "Allow UDP ingress to workers from internal load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(17)
  source                    = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  udp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_06" {
  description               = "Allow TCP egress from OKE control plane to pods"
  destination               = oci_core_network_security_group.nsg_pods_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_09" {
  description               = "Allow TCP ingress to kube-apiserver from operator instance"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_operator_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group" "nsg_pods_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "pods-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_04" {
  description               = "Allow TCP egress from workers to Kubernetes API server"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_00" {
  description               = "Allow TCP ingress from anywhere to HTTPS port"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 443
      min = 443
    }
  }
}

resource "oci_core_network_security_group" "nsg_bastion_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "bastion-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_04" {
  description               = "Allow UDP egress from public load balancers to workers nodes for NodePort traffic"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(17)
  stateless                 = false
  udp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group" "nsg_int_lb_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "int_lb-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_12" {
  description               = "Allow ALL ingress to workers from other workers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_workers_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_route_table" "rt_service_gw_route" {
  compartment_id = var.compartment_ocid
  display_name   = "service-gw-route"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  route_rules {
    description       = "Terraformed - Auto-generated at Service Gateway creation: All Services in region to Service Gateway"
    destination       = "all-iad-services-in-oracle-services-network"
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.sgw_service_gateway.id
    route_type        = "STATIC"
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_15" {
  description               = "Allow TCP ingress to workers from public load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_bastion_tbhcuw_rule_02" {
  description               = "Allow SSH egress from bastion to workers"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 22
      min = 22
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_03" {
  description               = "Allow TCP ingress from anywhere to HTTP port"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 80
      min = 80
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_00" {
  description               = "Allow ICMP ingress to pods for path discovery"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = jsonencode(1)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_subnet" "subnet_cp_tbhcuw" {
  cidr_block                 = "10.140.0.0/29"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "cp-tbhcuw"
  dns_label                  = "cp"
  ipv4cidr_blocks            = ["10.140.0.0/29"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = false
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.rt_internet_route.id
  security_list_ids          = [oci_core_security_list.sl_default_security_list_for_oke_test_vcn_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_subnet" "subnet_workers_tbhcuw" {
  cidr_block                 = "10.140.32.0/20"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "workers-tbhcuw"
  dns_label                  = "wo"
  ipv4cidr_blocks            = ["10.140.32.0/20"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = true
  prohibit_public_ip_on_vnic = true
  route_table_id             = oci_core_route_table.rt_nat_route.id
  security_list_ids          = [oci_core_security_list.sl_default_security_list_for_oke_test_vcn_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_subnet" "subnet_bastion_tbhcuw" {
  cidr_block                 = "10.140.0.8/29"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "bastion-tbhcuw"
  dns_label                  = "ba"
  ipv4cidr_blocks            = ["10.140.0.8/29"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = false
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.rt_internet_route.id
  security_list_ids          = [oci_core_security_list.sl_default_security_list_for_oke_test_vcn_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_internet_gateway" "igw_internet_gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "internet-gateway"
  enabled        = true
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_security_list" "sl_int_lb_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "int_lb-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_bastion_tbhcuw_rule_00" {
  description               = "Allow TCP egress from bastion to cluster endpoint"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_subnet" "subnet_pub_lb_tbhcuw" {
  cidr_block                 = "10.140.0.64/27"
  compartment_id             = var.compartment_ocid
  dhcp_options_id            = oci_core_dhcp_options.dhcp_default_dhcp_options_for_oke_test_vcn_tbhcuw.id
  display_name               = "pub_lb-tbhcuw"
  dns_label                  = "pu"
  ipv4cidr_blocks            = ["10.140.0.64/27"]
  ipv6cidr_blocks            = []
  prohibit_internet_ingress  = false
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.rt_internet_route.id
  security_list_ids          = [oci_core_security_list.sl_pub_lb_tbhcuw.id]
  vcn_id                     = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_int_lb_tbhcuw_rule_00" {
  description               = "Allow UDP egress from internal load balancers to workers for Node Ports"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  protocol                  = jsonencode(17)
  stateless                 = false
  udp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_05" {
  description               = "Allow TCP ingress to kube-apiserver from pods"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_pods_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_route_table" "rt_nat_route" {
  compartment_id = var.compartment_ocid
  display_name   = "nat-route"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  route_rules {
    description       = "Terraformed - Auto-generated at NAT Gateway creation: NAT Gateway as default gateway"
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_nat_gateway.nat_nat_gateway.id
    route_type        = "STATIC"
  }
  route_rules {
    description       = "Terraformed - Auto-generated at Service Gateway creation: All Services in region to Service Gateway"
    destination       = "all-iad-services-in-oracle-services-network"
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.sgw_service_gateway.id
    route_type        = "STATIC"
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_03" {
  description               = "Allow ALL egress from workers to internet"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_01" {
  description               = "Allow ICMP ingress for path discovery from worker nodes"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(1)
  source                    = oci_core_network_security_group.nsg_workers_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_bastion_tbhcuw_rule_01" {
  description               = "Allow SSH egress from bastion to operator"
  destination               = oci_core_network_security_group.nsg_operator_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 22
      min = 22
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_02" {
  description               = "Allow TCP ingress for Kubernetes control plane inter-communication"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_cp_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group" "nsg_pub_lb_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "pub_lb-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_05" {
  description               = "Allow TCP egress from public load balancers to workers nodes for NodePort traffic"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_nat_gateway" "nat_nat_gateway" {
  block_traffic  = false
  compartment_id = var.compartment_ocid
  display_name   = "nat-gateway"
  public_ip_id   = var.nat_nat_gateway_public_ip_id
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_01" {
  description               = "Allow ALL egress from pods to internet"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_00" {
  description               = "Allow ICMP egress from workers for path discovery"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(1)
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_03" {
  description               = "Allow ALL egress from pods to other pods"
  destination               = oci_core_network_security_group.nsg_pods_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}

resource "oci_core_network_security_group" "nsg_cp_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "cp-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group" "nsg_workers_tbhcuw" {
  compartment_id = var.compartment_ocid
  display_name   = "workers-tbhcuw"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
}

resource "oci_core_network_security_group_security_rule" "nsg_operator_tbhcuw_rule_03" {
  description               = "Allow TCP egress from operator to Kubernetes API server"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_operator_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_09" {
  description               = "Allow TCP ingress to workers from internal load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_07" {
  description               = "Allow TCP egress from workers to OCI Services"
  destination               = "all-iad-services-in-oracle-services-network"
  destination_type          = "SERVICE_CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_07" {
  description               = "Allow TCP egress from pods to OCI Services"
  destination               = "all-iad-services-in-oracle-services-network"
  destination_type          = "SERVICE_CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_16" {
  description               = "Allow ICMP ingress to workers for path discovery"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(1)
  source                    = "0.0.0.0/0"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_17" {
  description               = "Allow ALL ingress to workers from Kubernetes control plane for webhooks served by workers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_cp_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_pub_lb_tbhcuw_rule_01" {
  description               = "Allow TCP egress from public load balancers to worker nodes for health checks"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10256
      min = 10256
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_operator_tbhcuw_rule_00" {
  description               = "Allow ICMP ingress to operator from bastion for path discovery"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_operator_tbhcuw.id
  protocol                  = jsonencode(1)
  source                    = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_03" {
  description               = "Allow ICMP egress for path discovery to worker nodes"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(1)
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_08" {
  description               = "Allow TCP ingress to kube-apiserver from worker nodes"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_workers_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_06" {
  description               = "Allow ALL ingress to workers from pods"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_pods_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_10" {
  description               = "Allow TCP ingress to OKE control plane from pods"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_pods_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 12250
      min = 12250
    }
  }
}

resource "oci_core_route_table" "rt_internet_route" {
  compartment_id = var.compartment_ocid
  display_name   = "internet-route"
  vcn_id         = oci_core_vcn.vcn_oke_test_vcn_tbhcuw.id
  route_rules {
    description       = "Terraformed - Auto-generated at Internet Gateway creation: Internet Gateway as default gateway"
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.igw_internet_gateway.id
    route_type        = "STATIC"
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_int_lb_tbhcuw_rule_03" {
  description               = "Allow TCP egress from internal load balancers to workers for health checks"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10256
      min = 10256
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_int_lb_tbhcuw_rule_02" {
  description               = "Allow TCP ingress to internal load balancers from internal VCN/DRG"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  protocol                  = "all"
  source                    = "10.140.0.0/16"
  source_type               = "CIDR_BLOCK"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_08" {
  description               = "Allow ALL ingress to pods from other pods"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = "all"
  source                    = oci_core_network_security_group.nsg_pods_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
}

resource "oci_core_network_security_group_security_rule" "nsg_cp_tbhcuw_rule_11" {
  description               = "Allow TCP egress from OKE control plane to worker nodes"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_cp_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 12250
      min = 12250
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_int_lb_tbhcuw_rule_01" {
  description               = "Allow ICMP egress from internal load balancers to worker nodes for path discovery"
  destination               = oci_core_network_security_group.nsg_workers_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_int_lb_tbhcuw.id
  protocol                  = jsonencode(1)
  stateless                 = false
  icmp_options {
    code = 4
    type = 3
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_pods_tbhcuw_rule_09" {
  description               = "Allow TCP egress from pods to Kubernetes API server"
  destination               = oci_core_network_security_group.nsg_cp_tbhcuw.id
  destination_type          = "NETWORK_SECURITY_GROUP"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_pods_tbhcuw.id
  protocol                  = jsonencode(6)
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 6443
      min = 6443
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_18" {
  description               = "Allow UDP ingress to workers from public load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(17)
  source                    = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  udp_options {
    destination_port_range {
      max = 32767
      min = 30000
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_operator_tbhcuw_rule_01" {
  description               = "Allow SSH ingress to operator from bastion"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_operator_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_bastion_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 22
      min = 22
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_workers_tbhcuw_rule_14" {
  description               = "Allow TCP ingress to workers for health check from public load balancers"
  direction                 = "INGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_workers_tbhcuw.id
  protocol                  = jsonencode(6)
  source                    = oci_core_network_security_group.nsg_pub_lb_tbhcuw.id
  source_type               = "NETWORK_SECURITY_GROUP"
  stateless                 = false
  tcp_options {
    destination_port_range {
      max = 10256
      min = 10256
    }
  }
}

resource "oci_core_network_security_group_security_rule" "nsg_operator_tbhcuw_rule_02" {
  description               = "Allow ALL egress from operator to internet"
  destination               = "0.0.0.0/0"
  destination_type          = "CIDR_BLOCK"
  direction                 = "EGRESS"
  network_security_group_id = oci_core_network_security_group.nsg_operator_tbhcuw.id
  protocol                  = "all"
  stateless                 = false
}
