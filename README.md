# mxcat
Command-line tool concatenate MuseScore XML files (akin to UNIX cat behavior) or split MuseScore XML files on a finer staff-level basis (such as solely the upper staff on a two-staff piano part).
```
usage: mxcat.py [-h] [--output output] [--staff staves] [--count] [--debug]
                files [files ...]
```
* Merging was removed in MuseScore 3 because it was unstable, and there have been no successful attempts to revive it ([thread 1](https://musescore.org/en/node/291978), [thread 2](https://musescore.org/en/node/264845), [thread 3](https://musescore.org/en/node/264733), and so on... lead to dead ends). 
* Generating files is limited to individual parts in MuseScore, but `mxcat` extends this behavior to select staffs for each file. For instance, you could export the first 4 staves into a file, and the remaining 12 staves into another file. This isn't supported by MuseScore.

<p align="center">
  <img src="sample.gif" style="text-align: center" width="653px"/>
  </br>
  <i>Sample usage</i>
</p>

* In general, mxcat will concatentate Musescore XML files and print on the standard output; `mxcat`
behaves similarly to UNIX `cat`, where you may redirect output to another file.
You can pipe to cat if you want access to `cat`-like options (such as -n, -v,
and so on)
* Keep in mind that parsing multiple large mscx files will certainly take some time.
* `mxcat` does not (yet) have functionality to connect slurs and ties over different scores. If staff count is not constant over all files, you may find unexpected concatenation due to ambiguity while merging. Staves will be printed in order of increasing number.


## Sample usage:
Concatenate `file1.mscx`, and `file2.mscx`, and redirect output to `result.mscx`:
```bash
python mxcat.py file1.mscx file2.mscx > result.mscx
```

Concatenate several files, but only keep the first 2 staves. Then redirect the output into result.mscx.
```bash
python mxcat.py file*.mscx --staff 1,2 > result.mscx
```

Split `hamilton.mscx` into three parts: staves 1 and 2, then staves 3 and 4, then staves 15 and 16. Finally, save the output into `result_1,2.mscx`, `result_3,4.mscx`, and `result_15,16.mscx`. 
```bash
python mxcat.py hamilton.mscx --staff 1,2:3,4:15,16 --output helpless.mscx
```

Count the number of staves in `hamilton.mscx`:
```bash
python mxcat.py hamilton.mscx --count
```

Search debug comments:
```bash
python mxcat.py out*.mscx --debug | grep "\[DEBUG\]"
```

View help message:
```bash
python mxcat.py -h | less 
```

Numbered lines:
```bash
python mxcat.py file*.mscx | cat -n | less -S
```

## Detailed help:
```
usage: mxcat.py [-h] [--output output] [--staff staves] [--count] [--debug]
                files [files ...]

Concatenate Musescore XML files and print on the standard output; mxcat
behaves similarly to UNIX cat, where you may redirect output to another file.
You can pipe to cat if you want access to cat-like options (such as -n, -v,
and so on)

positional arguments:
  files            Files to concatenate.

optional arguments:
  -h, --help       show this help message and exit
  --output output  File to write to. Exists for cross-compatability and
                   multiple output. You can also use UNIX redirection >
                   output.mscx, instead of this argument.
  --staff staves   Colon and comma-separated staff-numbers to print across
                   multiple files, for instance --staff 0:1,2,3,4:5,6 will
                   create three files where the first file prints all parts,
                   the second file prints staves 1, 2, 3, and 4, while the
                   third file prints staves 5 and 6. The staff 0 indicates to
                   mxcat that it will print all parts. To save files, also
                   ensure that --output is set to a value. **Colon-separated
                   file output is experimental.** If multiple files are given,
                   mxcat will merge the files before printing.
  --count          Print number of staffs in the score, and exit. If multiple
                   files are given, only the first file will be parsed.
  --debug          Print debug comments into output, which is grep-able with
                   [DEBUG].

```
