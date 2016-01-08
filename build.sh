#!/bin/bash

# Update this to an absolute path if pycdc is not available on $PATH
decompyle_path="pycdc"

# The starting point for traversing the dir tree looking for .pyc files
input_dir="/Applications/Ableton\ Live\ 9\ Trial.app/Contents/App-Resources/MIDI\ Remote\ Scripts/Push2"
output_dir="Push2"

# Ensure output_dir tree exists
mkdir -p "${output_dir}"

function decompile {
  compiled_file_path="${1}"

  # Derive source file name from compiled_file_path, prefix with output_dir
  basename=${1##*/}
  prefix=${basename%.*}
  source_file_path="${output_dir}/${prefix}.py"
  "${decompyle_path}" "${compiled_file_path}" > "${source_file_path}"
}

# Start iterating over files
# Temporarily changing input file separator (IFS) from space to avoid issues
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for file in ${input_dir}/*; do
  echo "${file}"

  # Descend into directories
  if [[ -d ${file} ]]; then
    # TODO: Handle recursion
    echo "${file} is a directory"
  fi

  decompile "${file}"
done
# restore $IFS
IFS=$SAVEIFS
