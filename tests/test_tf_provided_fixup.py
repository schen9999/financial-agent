"""scripts/tf_provided_fixup.py drops only the named attributes of the named
resource types, including multi-line values."""
from scripts import tf_provided_fixup as fx

SRC = '''resource "oci_containerengine_node_pool" "p" {
  name                = "oke-cpu"
  quantity_per_subnet = 0
  subnet_ids = [
    "ocid1.subnet.x",
  ]
  node_config_details {
    size = 2
  }
}

resource "oci_core_subnet" "s" {
  subnet_ids = ["kept"]
}
'''


def test_drops_only_the_named_node_pool_fields():
    out, n = fx.fixup(SRC)
    assert n == 2
    assert "quantity_per_subnet" not in out and "ocid1.subnet.x" not in out
    assert 'subnet_ids = ["kept"]' in out and "node_config_details {" in out and "size = 2" in out
