# mxcat
Command-line tool to merge MuseScore XML files (akin to UNIX cat behavior).
* This feature is removed in MuseScore 3 because it was unstable, but there has been no such attempts to revive it ([thread 1](https://musescore.org/en/node/291978), [thread 2](https://musescore.org/en/node/264845), [thread 3](https://musescore.org/en/node/264733), and so on...). 
* I'm not too familiar with the XML syntax that MuseScore uses, but I gave it my best shot, in case someone out there had the same problems I did.
* In general, mxcat will concatentate Musescore XML files and print on the standard output; `mxcat`
behaves similarly to UNIX `cat`, where you may redirect output to another file.
You can pipe to cat if you want access to `cat`-like options (such as -n, -v,
and so on)
* Keep in mind that parsing multiple large mscx files will certainly take some time.
* `mxcat` has not (yet) implemented behavior to connect slurs and ties over different scores.

<p align="center">
  <img src="media/sample.gif" style="text-align: center" />
  </br>
  <i>Sample usage</i>
</p>

## Sample usage:

Concatenate several files:        
```bash
python mxcat.py file*.mscx > result.mscx
```

View help message:        
```bash
python mxcat.py -h | less 
```

Numbered lines:           
```bash
python mxcat.py file*.mscx | cat -n | less -S
```

Search debug comments:    
```bash
python mxcat.py out*.mscx --debug true | grep "\[DEBUG\]"
```
