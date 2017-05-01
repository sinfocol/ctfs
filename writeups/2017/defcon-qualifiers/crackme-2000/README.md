# DEF CON CTF QUALIFIERS 2017 - Crackme 2000

We are given with multiple binary files that receive a code from stdin and show a string based on whether the code was correct or not:

```bash
$ ./01dd90c3b7d9a36227a5ddc96c7887acbcb973744c1971eaa6da6cccc6c3e261 
enter code:
AAABBBCCCDDD
$ ./01dd90c3b7d9a36227a5ddc96c7887acbcb973744c1971eaa6da6cccc6c3e261 
enter code:
==== The meds helped 
sum is 12
```

You can download a [some samples](crackmes-2000-samples.zip) of the provided files, solution here includes:
* magic
* sorcery
* alchemy
* witchcraft

## TL;DR

grep ftw

```objdump -M intel -d magic/* | grep -P "cmp\s+rdi" | grep -oP "0x\w{1,2}" | xxd -r -p```

```objdump -M intel -d sorcery/* | grep -P " 3\w{3}.*cmp\s+[ac]l" | grep -oP "0x\w{1,2}" | xxd -r -p```

```objdump -M intel -d alchemy/* | grep -P " 4[012]\w{4}:.*cmp\s+r[ac]x,0x\w{2}$" | grep -oP "0x\w{1,2}" | xxd -r -p```

```objdump -M intel -d witchcraft/* | grep -P "[add|sub|cmp]\s+rdi,0x" | cut -c33-80 | sed 's/    /,/' | python parser.py```

## Solutions

This may not be an advanced solution but it was one of the fastest way that came to mind. Each one of the problems had a pattern that was easily grepable.

### magic

First binary follows this pattern for string comparison:

```asm
cmp rdi,0xhh
```

```asm
 93b:	48 83 ff 3d          	cmp    rdi,0x3d           // First char
 93f:	74 0e                	je     94f <_init+0x257>
 941:	48 83 ec 08          	sub    rsp,0x8
 945:	bf 01 00 00 00       	mov    edi,0x1
 94a:	e8 09 fe ff ff       	call   758 <_init+0x60>
 94f:	b8 16 00 00 00       	mov    eax,0x16
 954:	c3                   	ret    
 955:	48 83 ff 3d          	cmp    rdi,0x3d           // Second char
 959:	74 0e                	je     969 <_init+0x271>
 95b:	48 83 ec 08          	sub    rsp,0x8
 95f:	bf 02 00 00 00       	mov    edi,0x2
 964:	e8 ef fd ff ff       	call   758 <_init+0x60>
 969:	b8 43 00 00 00       	mov    eax,0x43
 96e:	c3                   	ret
```

We use objdump, grep, and xxd to get the solutions for the magic binaries:

```
objdump -M intel -d $file |
grep -P "cmp\s+rdi" |
grep -oP "0x\w{1,2}" |
xxd -r -p
```

```
$ for file in $(ls);do answer=$(objdump -M intel -d $file | grep -P "cmp\s+rdi" | grep -oP "0x\w{1,2}" | xxd -r -p);echo "'$file': '$answer',";done
'01dd90c3b7d9a36227a5ddc96c7887acbcb973744c1971eaa6da6cccc6c3e261': '==== The meds helped ',
'0af4913433ca0adc86ad2befd7ffe465239953364a8e1dcfbddbe05254bb8c25': 'de. On the last night, he presented me with a ',
'0c029d126ab043c1b5137f8ddece16af67857743cc1a8e0d496181f002861c04': 'han anyone -- shir',
```

We can send now the answers to the server using [magic.py](magic.py):

```
$ python magic.py
File:  5cd47c03c44ab6e407cc48a3ed0244d97e9a0cecc631ee981dad363845e73cfa
Answer:  LCBjb21tb24gbGF3IHJpZ2h0cyBv
...
File:  550d4a3c0add395524dabaa290929a040dadafb3f54740575e3cf43ea8dfddb3
Answer:  IGFuZCB0aGUgaG91c2Ugdw==
FLAG:  The flag is: a color map of the sun sokemsUbif
```

### sorcery

Sorcery binaries follow a similar pattern with a slight modification at the end:

```asm
3hhh: cmp [ac]l,0xhh
```

```asm
    36a5:	80 f9 67             	cmp    cl,0x67                                 // First char
    36a8:	0f 85 76 03 00 00    	jne    3a24 <pthread_mutex_lock@plt+0xe94>
    36ae:	48 83 f8 01          	cmp    rax,0x1
    36b2:	0f 84 f8 02 00 00    	je     39b0 <pthread_mutex_lock@plt+0xe20>
    36b8:	8a 4f 01             	mov    cl,BYTE PTR [rdi+0x1]
    36bb:	80 f9 20             	cmp    cl,0x20                                 // Second char
    36be:	0f 85 6c 03 00 00    	jne    3a30 <pthread_mutex_lock@plt+0xea0>
    36c4:	48 83 f8 02          	cmp    rax,0x2
    36c8:	0f 84 e2 02 00 00    	je     39b0 <pthread_mutex_lock@plt+0xe20>
    36ce:	8a 4f 02             	mov    cl,BYTE PTR [rdi+0x2]
    ...
    3935:	3c 50                	cmp    al,0x50                                 // Last char
    3937:	0f 85 4f 02 00 00    	jne    3b8c <pthread_mutex_lock@plt+0xffc>
```

The second command used was:

```
objdump -M intel -d $file |
grep -P " 3\w{3}.*cmp\s+[ac]l" |
grep -oP "0x\w{1,2}" |
xxd -r -p
```

```
$ for file in $(ls);do answer=$(objdump -M intel -d $file | grep -P " 3\w{3}.*cmp\s+[ac]l" | grep -oP "0x\w{1,2}" | xxd -r -p);echo "'$file': '$answer',";done
'02a1deee284afc3acd59d1b68cf5c9ad40e4ccf47ba99db55e38df8f1136ef5e': 'g plans, dictating voicemail. P',
'02a72b19e546bc4ef56610c1f5c200ccef462907241a22909fbe341da20d92a2': 'assed it to me',
'0a4def1cae72a724e81042f7565182ca70b7ffb2de9314bd6380b03c42e9bb84': 'elt his ',
```

Using [sorcery.py](sorcery.py) we can get the flag for the problem:

```
$ python sorcerer.py
File:  5c28784fd1e7e89499e8180be9325e0b8b10390ff85bb66d7ca5cdbf1c9b66d4
Answer:  IGNhcmVmdWxs
...
File:  eeb4f76a92eda100ea7dbebd2c16136826b1614f3635f93488dafcda597af099
Answer:  eSB2aXNpdCB0aGlzIHBsYWNlIGZvciA=
FLAG:  The flag is: don't forget me when you're famous Klousovnec
```

### alchemy

Following the same reasoning we can find the pattern for this binary which is similar to the sorcery pattern:

```asm
4[012]hhhh: cmp r[ca]x,0hh
```

```asm
  40f1b4:	48 83 f9 65          	cmp    rcx,0x65                        // First char
  40f1b8:	0f 85 93 09 00 00    	jne    40fb51 <_start@@Base+0x24e1>
  40f1be:	41 83 ff 01          	cmp    r15d,0x1
  40f1c2:	0f 8e 2f 09 00 00    	jle    40faf7 <_start@@Base+0x2487>
  40f1c8:	0f b6 48 01          	movzx  ecx,BYTE PTR [rax+0x1]
  40f1cc:	48 83 f9 20          	cmp    rcx,0x20                        // Second char
  40f1d0:	0f 85 88 09 00 00    	jne    40fb5e <_start@@Base+0x24ee>
  40f1d6:	41 83 ff 02          	cmp    r15d,0x2
  40f1da:	0f 8e 17 09 00 00    	jle    40faf7 <_start@@Base+0x2487>
  40f1e0:	0f b6 48 02          	movzx  ecx,BYTE PTR [rax+0x2]
  ...
  40f5a4:	48 83 f8 65          	cmp    rax,0x65                        // Last char
  40f5a8:	0f 85 c5 07 00 00    	jne    40fd73 <_start@@Base+0x2703>
```

The command for this problem is:

```
objdump -M intel -d $file |
grep -P " 4[012]\w{4}:.*cmp\s+r[ac]x,0x\w{2}$" |
grep -oP "0x\w{1,2}" |
xxd -r -p
```

```
# for file in $(ls);do answer=$(objdump -M intel -d $file | grep -P " 4[012]\w{4}:.*cmp\s+r[ac]x,0x\w{2}$" | grep -oP "0x\w{1,2}" | xxd -r -p);echo "'$file': '$answer',";done
'04b7f46deed1405c91d155e535ddd744176611b0b9f0d28962c6025822d34bf8': 'e up the steeplechase and she had the dogle',
'04bff69a80594bfd1b8b4d57f87a2fb80a6cca2eb3582997fe61a97b4f8164ad': ', as far as possible from Dan. He was working h',
'0b96430f0a2d8960ae9116db3a1cb580b56ba9a74bfdd0ba74ad3cfff6778a9a': 'issioned their work. Suneep l',
```

Using [alchemy.py](alchemy.py) we were able to get the flag:

```
$ python alchemy.py
File:  762ad3727e8be06b6b10f94291f63028b26328500092c52523f3f13544cce639
Answer:  IGF3YXkgaW4gdGhlIHJhcg==
...
File:  def7fcc4e930d34cb98ab1d7c922a3eaab60d5ed6495d067569dcff5012ca523
Answer:  dmVuIGNhd2VkLCBN
FLAG:  The flag is: end of the world sun clyigujheo
```

### witchcraft

Witchcraft does not follow a so simple pattern as seen before, instead it uses additions and substractions to calculate a proper value for each character, however the pattern was:

```asm
add rdi,0xhh
sub rdi,0xhh
...
cmp rdi,0xhh
```

```asm
  402120:	55                   	push   rbp
  402121:	48 89 e5             	mov    rbp,rsp
  402124:	48 85 ff             	test   rdi,rdi      // First char
  402127:	0f 84 28 01 00 00    	je     402255 <_TTSfq4n_s___TFVs11_StringCore15_encodeSomeUTF8fT4fromSi_TSiVs6UInt64_@plt+0xf75>
  40212d:	48 83 c7 14          	add    rdi,0x14
  402131:	0f 80 28 01 00 00    	jo     40225f <_TTSfq4n_s___TFVs11_StringCore15_encodeSomeUTF8fT4fromSi_TSiVs6UInt64_@plt+0xf7f>
  402137:	48 83 c7 1f          	add    rdi,0x1f
  ...
  402245:	48 81 ff c5 00 00 00 	cmp    rdi,0xc5     // Calculated char comparison
  40224c:	75 07                	jne    402255 <_TTSfq4n_s___TFVs11_StringCore15_encodeSomeUTF8fT4fromSi_TSiVs6UInt64_@plt+0xf75>
  40224e:	b8 c5 00 00 00       	mov    eax,0xc5
  402253:	5d                   	pop    rbp
  402254:	c3                   	ret 
```

The [parser.py](parser.py) script was used to calculate the initial state of each character:

```python
import sys

values = []
for line in sys.stdin:
    op, dummy, val = line.split(',')

    if val.find('ffffffffffffff') != -1:
        val = (256 - int(val.replace('ffffffffffffff', ''), 16)) * -1
    else:
        val = int(val, 16)
    
    if op == 'cmp':
        result = val
        for value in values:
            result = result + value
        sys.stdout.write(chr(result))
        
        values = []
    else:
        if op == 'add':
            val = val * -1
            
        values = values + [val]
```

The command used to get the string for each binary was:

```
objdump -M intel -d $file |
grep -P "[add|sub|cmp]\s+rdi,0x" |
cut -c33-80 |
sed 's/    /,/' |
python parser.py
```

```
$ for file in $(ls);do answer=$(objdump -M intel -d $file | grep -P "[add|sub|cmp]\s+rdi,0x" | cut -c33-80 | sed 's/    /,/' | python parser.py);echo "'$file': '$answer',";done
'01b22b4c67a408a08c07b7c3af5a807512cc6dc41380d889f14605dc3bbcda43': 'y Cast. She vanishes, then reappears, forty ',
'02bd830274ed4a6550456eb092a5124701d1d1216bea20ee86e70f7a78ef1729': ' down to work for me, they're all real',
'03b2dcde6fbc4f9cb96ce1de4cbccd73960c196f6345e6dee66da0a9a89bf2d0': ' did the',
```

Finally, the [witchcraft.py](witchcraft.py) was used to get the final flag:

```
$ python witchcraft.py
File:  6577fdb2474b1a499922c6544b0c1888eedb28e6d48d0003d958dfa24ac16c08
Answer:  VG9uaWdodC4gQWZ0
...
File:  da92359b736fdc3d0d1c7688e9ebd02b67406d4260823514cd849eaed0ec9c13
Answer:  IG9mIHlvdXIgdm9sdW50YXJ5IG5lcnZvdXMgcHJvYw==
FLAG:  The flag is: bustin makes me feel good scengoybEm
```

## Flags

### magic
> a color map of the sun sokemsUbif

### sorcery
> don't forget me when you're famous Klousovnec

### alchemy
> end of the world sun clyigujheo

### witchcraft
> bustin makes me feel good scengoybEm