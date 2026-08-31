# VCN and subnets for OKE, following Oracle's reference layout for a public
# API endpoint with private workers:
#   10.0.0.0/28  api      public  — Kubernetes API endpoint
#   10.0.1.0/24  workers  private — both node pools (egress via NAT + SGW)
#   10.0.2.0/24  lb       public  — OCI load balancers for exposed Services

locals {
  vcn_cidr     = "10.0.0.0/16"
  api_cidr     = "10.0.0.0/28"
  workers_cidr = "10.0.1.0/24"
  lb_cidr      = "10.0.2.0/24"
}

resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_ocid
  display_name   = "${var.project}-vcn"
  cidr_blocks    = [local.vcn_cidr]
  dns_label      = "finagent"
  freeform_tags  = local.tags
}

# --- Gateways ---

resource "oci_core_internet_gateway" "igw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-igw"
}

resource "oci_core_nat_gateway" "nat" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-nat"
}

# "All services" service gateway: private workers reach OCIR, Object Storage,
# and the OKE control-plane services without traversing the NAT.
data "oci_core_services" "all" {
  filter {
    name   = "name"
    values = ["All .* Services In Oracle Services Network"]
    regex  = true
  }
}

resource "oci_core_service_gateway" "sgw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-sgw"

  services {
    service_id = data.oci_core_services.all.services[0].id
  }
}

# --- Route tables ---

resource "oci_core_route_table" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-rt-public"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.igw.id
  }
}

resource "oci_core_route_table" "private" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-rt-private"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_nat_gateway.nat.id
  }

  route_rules {
    destination       = data.oci_core_services.all.services[0].cidr_block
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.sgw.id
  }
}

# --- Security lists (Oracle's documented OKE rule set, trimmed to this topology) ---

resource "oci_core_security_list" "api" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-seclist-api"

  # kubectl / CI access to the API endpoint
  ingress_security_rules {
    protocol = "6" # TCP
    source   = var.api_allowed_cidr
    tcp_options {
      min = 6443
      max = 6443
    }
  }

  # Workers -> API server
  ingress_security_rules {
    protocol = "6"
    source   = local.workers_cidr
    tcp_options {
      min = 6443
      max = 6443
    }
  }

  # Workers -> control plane (OKE internal)
  ingress_security_rules {
    protocol = "6"
    source   = local.workers_cidr
    tcp_options {
      min = 12250
      max = 12250
    }
  }

  # Path MTU discovery
  ingress_security_rules {
    protocol = "1" # ICMP
    source   = local.workers_cidr
    icmp_options {
      type = 3
      code = 4
    }
  }

  egress_security_rules {
    protocol    = "6"
    destination = local.workers_cidr
  }

  egress_security_rules {
    protocol         = "6"
    destination      = data.oci_core_services.all.services[0].cidr_block
    destination_type = "SERVICE_CIDR_BLOCK"
    tcp_options {
      min = 443
      max = 443
    }
  }

  egress_security_rules {
    protocol    = "1"
    destination = local.workers_cidr
    icmp_options {
      type = 3
      code = 4
    }
  }
}

resource "oci_core_security_list" "workers" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-seclist-workers"

  # Pod-to-pod / node-to-node (flannel overlay)
  ingress_security_rules {
    protocol = "all"
    source   = local.workers_cidr
  }

  # Control plane -> kubelet et al.
  ingress_security_rules {
    protocol = "6"
    source   = local.api_cidr
  }

  # Path MTU discovery
  ingress_security_rules {
    protocol = "1"
    source   = "0.0.0.0/0"
    icmp_options {
      type = 3
      code = 4
    }
  }

  # Load balancer -> NodePorts and kube-proxy health checks
  ingress_security_rules {
    protocol = "6"
    source   = local.lb_cidr
    tcp_options {
      min = 30000
      max = 32767
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = local.lb_cidr
    tcp_options {
      min = 10256
      max = 10256
    }
  }

  # Image pulls (NAT), OCI services (SGW), API endpoint — allow all egress.
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
  }
}

resource "oci_core_security_list" "lb" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project}-seclist-lb"

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }

  egress_security_rules {
    protocol    = "6"
    destination = local.workers_cidr
    tcp_options {
      min = 30000
      max = 32767
    }
  }

  egress_security_rules {
    protocol    = "6"
    destination = local.workers_cidr
    tcp_options {
      min = 10256
      max = 10256
    }
  }
}

# --- Subnets ---

resource "oci_core_subnet" "api" {
  compartment_id             = var.compartment_ocid
  vcn_id                     = oci_core_vcn.main.id
  display_name               = "${var.project}-subnet-api"
  cidr_block                 = local.api_cidr
  dns_label                  = "api"
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.public.id
  security_list_ids          = [oci_core_security_list.api.id]
}

resource "oci_core_subnet" "workers" {
  compartment_id             = var.compartment_ocid
  vcn_id                     = oci_core_vcn.main.id
  display_name               = "${var.project}-subnet-workers"
  cidr_block                 = local.workers_cidr
  dns_label                  = "workers"
  prohibit_public_ip_on_vnic = true
  route_table_id             = oci_core_route_table.private.id
  security_list_ids          = [oci_core_security_list.workers.id]
}

resource "oci_core_subnet" "lb" {
  compartment_id             = var.compartment_ocid
  vcn_id                     = oci_core_vcn.main.id
  display_name               = "${var.project}-subnet-lb"
  cidr_block                 = local.lb_cidr
  dns_label                  = "lb"
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.public.id
  security_list_ids          = [oci_core_security_list.lb.id]
}
