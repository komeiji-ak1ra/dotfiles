# user function

function chmod_reset() {
    find -type f -exec chmod 0644 {} \;
    find -type d -exec chmod 0755 {} \;
}

export -f chmod_reset