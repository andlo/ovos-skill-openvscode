#/bin/bash
type=$1
download=$(curl -s https://api.github.com/repos/coder/code-server/releases/latest | jq -r ".assets[] | select(.name | test(\"${type}\")) | .browser_download_url")
filename=$(curl -s https://api.github.com/repos/coder/code-server/releases/latest | jq -r ".assets[] | select(.name | test(\"${type}\")) | .name")
wget -q $download
if [ -f $filename ]; then
    mkdir code-server
    tar -zxf $filename --strip-components=1 -C code-server
    rm $filename
fi
