# Outfoxed
## Building
The base changeset of the Firefox build is `655554:f4922b9e9a6b`, with a short (log)[./log] provided.
The (mozconfig file)[./mozconfig] used to build the challenge is also provided.

## Environment
The challenge is run with the content sandbox disabled:
`MOZ_DISABLE_CONTENT_SANDBOX ./firefox`


```bash
wget "http://ftp.gnu.org/gnu/gdb/gdb-8.3.tar.gz"
tar -xvzf gdb-8.3.tar.gz
cd gdb-8.3
./configure > /dev/null
make	> /dev/null
make install	> /dev/null
bash -c "$(curl -fsSL http://gef.blah.cat/sh)"
wget https://libc.blukat.me/d/libc6_2.29-0ubuntu2_amd64.so -O /lib/x86_64-linux-gnu/libm.so.6
chmod +x /lib/x86_64-linux-gnu/libm.so.6
cd /root
wget https://files.be.ax/outfoxed-7d11ebc85cf45e851977eda017da26ad71b225ecf28e3f2973fc1cbd09dd3286/outfoxed.tar.gz 
tar -xvf  outfoxed*> /dev/null
cd /root/firefox
gdb ./firefox -q
```