import os
import shutil
import subprocess
import sys
import tempfile

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

dependent_dir = os.path.abspath("../bin/dependent")

def fetch_and_extract(draft, version, modules):
    # Download the draft once, extract all of its modules into a
    # scratch directory, and copy over the ones that are needed.
    # A module name matches any extracted file that starts with it,
    # e.g., 'ietf-bgp' also picks up the ietf-bgp-* submodules.
    draft_version = draft + "-" + version
    print("Fetching " + draft_version)
    workdir = tempfile.mkdtemp()
    try:
        subprocess.run(["curl", "-sfO",
                        "https://www.ietf.org/archive/id/%s.txt"
                        % draft_version],
                       cwd=workdir, check=True)
        print("Extracting modules from " + draft_version)
        subprocess.run(["xym", draft_version + ".txt"],
                       cwd=workdir, check=True,
                       stdout=subprocess.DEVNULL)
        extracted = [f for f in os.listdir(workdir) if f.endswith(".yang")]
        needed = set()
        for module in modules:
            matches = [f for f in extracted if f.startswith(module)]
            if not matches:
                sys.exit("Module %s not found in %s"
                         % (module, draft_version))
            needed.update(matches)
        for f in sorted(needed):
            print("Copying " + f + " to ../bin/dependent/")
            shutil.copy(os.path.join(workdir, f), dependent_dir)
    finally:
        shutil.rmtree(workdir)

def fetch(module, path):
    file = path + module + ".yang.txt"
    print("Fetching file " + file)
    os.system('curl -sO http://%s' %file)
    model = module + ".yang"
    print("Moving module " + model + " to ../bin/dependent/")
    os.system("mv '%s'.txt ../bin/dependent/'%s'" %(model, model))

os.makedirs(dependent_dir, exist_ok=True)

# Group the modules by draft and version, so that each draft is
# downloaded only once.
drafts = {}
for module, draft, version in list_of_ietf_models:
    drafts.setdefault((draft, version), []).append(module)

for (draft, version), modules in drafts.items():
    fetch_and_extract(draft, version, modules)

# for list in list_of_ieee_models:
#    module, path = list
#    print(module)
#    fetch(module, path)
