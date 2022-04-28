#!/bin/sh

#
# Does the user have all the IETF published models.
#
if [ ! -d ../bin/iana/yang-parameters ]; then
   rsync -avz --delete rsync.iana.org::assignments/yang-parameters ../bin/iana/
fi

#
# Download dependent modules.
#
if [ ! -d ../bin/dependent ]; then
    python download-dependent-models.py
fi

for i in ../bin/ietf-*\@$(date +%Y-%m-%d).yang
do
    name=$(echo $i | cut -f 1-3 -d '.')
    echo "Validating $name.yang"
    if test "${name#^example}" = "$name"; then
        response=`pyang --ietf --lint --strict --canonical -p ../bin/iana/yang-parameters -p ../bin -f tree --max-line-length=72 --tree-line-length=69 $name.yang > $name-tree.txt.tmp`
    else            
        response=`pyang --ietf --strict --canonical -p ../bin/iana/yang-parameters -p ../bin -f tree --max-line-length=72 --tree-line-length=69 $name.yang > $name-tree.txt.tmp`
    fi
    if [ $? -ne 0 ]; then
        printf "$name.yang failed pyang validation\n"
        printf "$response\n\n"
        echo
	rm yang/*-tree.txt.tmp
        exit 1
    fi
    fold -w 71 $name-tree.txt.tmp > $name-tree.txt
    response=`yanglint -p ../bin/iana/yang-parameters -p ../bin $name.yang -i`
    if [ $? -ne 0 ]; then
        printf "$name.yang failed yanglint validation\n"
        printf "$response\n\n"
        echo
        exit 1
    fi
done
rm ../bin/*-tree.txt.tmp

# Generate a sub-tree with a depth of 3

for i in ../bin/ietf-bgp-ls\@$(date +%Y-%m-%d).yang
do
    name=$(echo $i | cut -f 1-3 -d '.')
    echo "Generating abridged tree diagram for $name.yang"
    if test "${name#^example}" = "$name"; then
       response=`pyang --lint --strict --canonical -p ../bin -p ../bin/iana/yang-parameters -f tree --tree-depth=3 --max-line-length=72 --tree-line-length=69 $name.yang > $name-sub-tree.txt.tmp`
    else            
        response=`pyang --ietf --strict --canonical -p ../bin -p ../bin/iana/yang-parameters -f tree --tree-depth=3 --max-line-length=72 --tree-line-length=69 $name.yang > $name-sub-tree.txt.tmp`
    fi
    if [ $? -ne 0 ]; then
        printf "$name.yang failed generation of sub-tree diagram\n"
        printf "$response\n\n"
        echo
	rm yang/*-sub-tree.txt.tmp
        exit 1
    fi
    fold -w 71 $name-sub-tree.txt.tmp > $name-sub-tree.txt
done
rm ../bin/*-sub-tree.txt.tmp

echo "Validating examples"

#for i in yang/example-bgp-ls-configuration-a.*.xml
#do
#    name=$(echo $i | cut -f 1-3 -d '.')
#    echo "Validating $name.xml"
#    response=`yanglint -ii -t config -p ../bin/iana/yang-parameters/ -p ../bin/iana/yang-parameters/ietf-network-instance@2019-01-21.yang ../bin/iana/yang-parameters/ietf-bgp@2022-02-04.yang ../bin/ietf-srv6-mobile\@$(date +%Y-%m-%d).yang $name.xml`
#    if [ $? -ne 0 ]; then
#       printf "failed (error code: $?)\n"
#       printf "$response\n\n"
#       echo
#       exit 1
#    fi
#done
