import os

list_of_ietf_models =\
[ 
  ["ietf-if-extensions", "draft-ietf-netmod-intf-ext-yang", "10"],
  ["ietf-if-vlan-encapsulation", "draft-ietf-netmod-sub-intf-vlan-model", "07"],
  ["ietf-if-flexible-encapsulation", "draft-ietf-netmod-sub-intf-vlan-model", "07"],
  ["ietf-yang-semver", "draft-ietf-netmod-yang-semver", "29"],
    ["iana-bgp-afi-safi-types", "draft-ietf-idr-bgp-model", "22"],
    ["iana-bgp-capabilities", "draft-ietf-idr-bgp-model", "22"],
    ["iana-bgp-community-types", "draft-ietf-idr-bgp-model", "22"],
    ["iana-bgp-notification", "draft-ietf-idr-bgp-model", "22"],
    ["iana-bgp-rib-types", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-capabilities", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-common", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-common-errors", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-common-multiprotocol", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-community-types", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-neighbor", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-policy", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-rib", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-rib-attributes", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-rib-tables", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-session-security", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp-types", "draft-ietf-idr-bgp-model", "22"],
    ["ietf-bgp", "draft-ietf-idr-bgp-model", "22"]
]


list_of_ieee_models =\
    [ ["ieee802-dot1q-types", "www.ieee802.org/1/files/public/YANGs/"] ]

def fetch_and_extract(draft, module, version):
    print("Fetching file " + draft + " with version " + version)
    draft_version = draft + "-" + version
    print(draft_version)
    os.system('curl -sO https://www.ietf.org/archive/id/%s.txt' %draft_version)
    print("Extracting Module from " + draft_version)
    os.system('xym %s.txt' %draft_version)
    print("Moving module " + module + " to ../bin/dependent/")
    os.system('mv %s* ../bin/dependent/' %module)
    print("Cleaning up ...")
    os.system('rm %s.txt' %draft_version)

def fetch(module, path):
    file = path + module + ".yang.txt"
    print("Fetching file " + file)
    os.system('curl -sO http://%s' %file)
    model = module + ".yang"
    print("Moving module " + model + " to ../bin/dependent/")
    os.system("mv '%s'.txt ../bin/dependent/'%s'" %(model, model))

os.system("mkdir -p ../bin/dependent")

for list in list_of_ietf_models:
    module, draft, version = list
    print(module)
    fetch_and_extract(draft, module, version)

# for list in list_of_ieee_models:
#    module, path = list
#    print(module)
#    fetch(module, path)

os.system('rm *.yang')
