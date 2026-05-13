#!/usr/bin/env fish

set ref_dir "./proto/referee"
set sim_dir "./proto/simulation"
set output_dir "./strategy/src/proto/"

# create proto folder in output directory if not exists
if [ ! -d "$output_dir" ]
    mkdir -p "$output_dir"
end

# create referee python file
for file in $ref_dir/*.proto
    protoc --proto_path="$ref_dir" --python_out="$output_dir" "$file"
end

# create simulation python file
for file in $sim_dir/*.proto
    protoc --proto_path="$sim_dir" --python_out="$output_dir" "$file"
end

# Fix python imports to use relative imports
sed -i -E 's/^import (.*)_pb2/from . import \1_pb2/g' "$output_dir"/*.py