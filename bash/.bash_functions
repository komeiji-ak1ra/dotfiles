# custom bash function

function sha256list {
    local dir="$1"
    local checksum="$(basename $dir).sha256"

    if [ -d "$dir" ]; then
        pushd "$dir"
        find . -type f -print0 |
            parallel -0 --max-lines=1 sha256sum "{}" | tee -a "../$checksum"
        popd
        LANG=C.UTF-8 sort -k2 "$checksum" >"${checksum}.sorted"
        mv "${checksum}.sorted" "$checksum"
    fi
}

function gen_list {
    local dir="$1"
    local list="$(basename $dir).list"

    if [ -d "$dir" ]; then
        pushd "$dir"
        find . -type f | LANG=C.UTF-8 sort | tee "../$list"
        popd
    fi
}

function check_exec() {
    for exe in $@; do
        hash "$exe" 2>/dev/null || {
            echo >&2 "Required command '$exe' is not installed. Aborting."
            exit 1
        }
    done
}
