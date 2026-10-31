#!/usr/bin/env fish
# Safely import the ESKD v2 package archive into this repository.
# Usage: fish scripts/import_eskd_v2_archive.fish /path/to/gazo_eskd_v2_implementation.tar.gz

if test (count $argv) -ne 1
    echo "Usage: fish scripts/import_eskd_v2_archive.fish /path/to/gazo_eskd_v2_implementation.tar.gz" >&2
    exit 2
end

set -l archive (realpath "$argv[1]" 2>/dev/null)
if test $status -ne 0; or not test -f "$archive"
    echo "ERROR: archive not found: $argv[1]" >&2
    exit 2
end

set -l repo_root (git rev-parse --show-toplevel 2>/dev/null)
if test $status -ne 0
    echo "ERROR: run this script from inside the repository." >&2
    exit 2
end

set -l temp_dir (mktemp -d)
if test $status -ne 0
    echo "ERROR: could not create temporary directory." >&2
    exit 2
end

tar -xzf "$archive" -C "$temp_dir"
if test $status -ne 0
    rm -rf "$temp_dir"
    echo "ERROR: archive extraction failed." >&2
    exit 1
end

set -l required_paths \
    "$temp_dir/cad/project_modification_eskd" \
    "$temp_dir/data/project_modification_reference.md" \
    "$temp_dir/gazo_layout.xml" \
    "$temp_dir/gazo_erc.txt"

for path in $required_paths
    if not test -e "$path"
        rm -rf "$temp_dir"
        echo "ERROR: required archive entry is missing: $path" >&2
        exit 1
    end
end

set -l destinations \
    "$repo_root/cad/project_modification_eskd" \
    "$repo_root/data/project_modification_reference.md" \
    "$repo_root/gazo_layout.xml" \
    "$repo_root/gazo_erc.txt"

for path in $destinations
    if test -e "$path"
        rm -rf "$temp_dir"
        echo "ERROR: refusing to overwrite existing path: $path" >&2
        exit 1
    end
end

mkdir -p "$repo_root/cad" "$repo_root/data"
or begin
    rm -rf "$temp_dir"
    echo "ERROR: could not create destination directories." >&2
    exit 1
end

cp -a "$temp_dir/cad/project_modification_eskd" "$repo_root/cad/"
and cp -a "$temp_dir/data/project_modification_reference.md" "$repo_root/data/"
and cp -a "$temp_dir/gazo_layout.xml" "$repo_root/"
and cp -a "$temp_dir/gazo_erc.txt" "$repo_root/"

if test $status -ne 0
    rm -rf "$temp_dir"
    echo "ERROR: import failed. Inspect git status and remove only partially copied ESKD v2 paths before retrying." >&2
    exit 1
end

# Keep the original converted GOST library sources available for the later
# symbol-migration step, without polluting the repository root.
set -l legacy_dir "$repo_root/cad/project_modification_eskd/legacy_library"
mkdir -p "$legacy_dir"
for name in Device_GOST.lib Device_GOST.dcm Diode_GOST.lib Diode_GOST.dcm Transistor_BJT_GOST.lib Transistor_BJT_GOST.dcm
    if test -f "$temp_dir/$name"
        cp -a "$temp_dir/$name" "$legacy_dir/"
    end
end

rm -rf "$temp_dir"
echo "ESKD v2 package imported. Review the working tree before committing:"
git -C "$repo_root" status --short
