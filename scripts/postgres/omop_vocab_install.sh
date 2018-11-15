#!/bin/bash

# This script needs to be run from a directory where the Athena standard vocabulary files exist.
declare -a arr=(
    "VOCABULARY.csv"
    "DRUG_STRENGTH.csv"
    "CONCEPT_CLASS.csv"
    "DOMAIN.csv" 
    "CONCEPT.csv"
    "CONCEPT_RELATIONSHIP.csv"
    "CONCEPT_ANCESTOR.csv" 
    "CONCEPT_SYNONYM.csv"
    "RELATIONSHIP.csv")
for i in "${arr[@]}"
do
    if [ ! -f "$i" ]; then
        echo "File not found! $i"
        NOT_ALL_FOUND=1
    fi
done
if [ ! -z ${NOT_ALL_FOUND+x} ]; then 
    echo "Exiting"
    exit 127
fi

# Test for existence of needed commands
command -v psql >/dev/null 2>&1 || { echo >&2 "This script requires psql, but it's not installed. Aborting."; exit 1; }
command -v pv >/dev/null 2>&1 || { echo >&2 "This script requires pv, but it's not installed. Aborting."; exit 1; }

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h)
    SERVER="$2"
    shift
    shift
    ;;
    -U)
    USERNAME="$2"
    shift
    shift
    ;;
esac
done

SERVER="${SERVER:-localhost}"
USERNAME="${USERNAME:-$USER}"

echo SERVER = "${SERVER}"
echo USERNAME = "${USERNAME}"

# Safely request password
stty -echo
printf "Enter password for user ${USERNAME}: "
read PASSWORD
stty echo
printf "\n"

# Erase the old vocabulary
# This uses DELETE instead of TRUNCATE, because TRUNCATE ignores the session_replication_role setting
PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica;
DELETE FROM CONCEPT;
DELETE FROM DRUG_STRENGTH;
DELETE FROM CONCEPT_RELATIONSHIP;
DELETE FROM CONCEPT_ANCESTOR;
DELETE FROM CONCEPT_SYNONYM;
DELETE FROM VOCABULARY;
DELETE FROM RELATIONSHIP;
DELETE FROM DOMAIN;
DELETE FROM CONCEPT_CLASS;
SET session_replication_role = DEFAULT;"

# Compact the db
PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "VACUUM;"

# Using `pv foo.csv | psql -c copy foo from stdin` lets you see a progress meter
pv VOCABULARY.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY VOCABULARY (vocabulary_id,vocabulary_name,vocabulary_reference,vocabulary_version,vocabulary_concept_id) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv DRUG_STRENGTH.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY DRUG_STRENGTH (drug_concept_id,ingredient_concept_id,amount_value,amount_unit_concept_id,numerator_value,numerator_unit_concept_id,denominator_value,denominator_unit_concept_id,box_size,valid_start_date,valid_end_date,invalid_reason) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv CONCEPT_CLASS.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY CONCEPT_CLASS (concept_class_id,concept_class_name,concept_class_concept_id) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv DOMAIN.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY DOMAIN (domain_id,domain_name,domain_concept_id) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv CONCEPT.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY CONCEPT (concept_id,concept_name,domain_id,vocabulary_id,concept_class_id,standard_concept,concept_code,valid_start_date,valid_end_date,invalid_reason) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv CONCEPT_RELATIONSHIP.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY CONCEPT_RELATIONSHIP (concept_id_1,concept_id_2,relationship_id,valid_start_date,valid_end_date,invalid_reason) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv CONCEPT_ANCESTOR.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY CONCEPT_ANCESTOR (ancestor_concept_id,descendant_concept_id,min_levels_of_separation,max_levels_of_separation) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv CONCEPT_SYNONYM.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY CONCEPT_SYNONYM (concept_id,concept_synonym_name,language_concept_id) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"
pv RELATIONSHIP.csv | PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "SET session_replication_role = replica; COPY RELATIONSHIP (relationship_id,relationship_name,is_hierarchical,defines_ancestry,reverse_relationship_id,relationship_concept_id) FROM STDIN WITH DELIMITER E'\t' CSV HEADER QUOTE E'\b'; SET session_replication_role = DEFAULT;"

# Compact the db
PGPASSWORD="${PASSWORD}" psql -h "${SERVER}" -U "${USERNAME}" -d omop --echo-all -c "VACUUM;"
