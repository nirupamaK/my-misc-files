Following are steps and instructions for running print-random-nums CLI utility for Linux and MacOS terminal.

1. The `print-random-nums` is a python3 based utility, however if you do not have python3 installed on system
   this can be run in python2.7 also which is default as of now for most of distributions, with a small change in the top most shebang line in the script:

        ```
        #!/usr/bin/env python3
        ```
   to 

        ```
        #!/usr/bin/env python
        ```

2. Copy the `print-random-nums.py` to /usr/local/bin directory as `print-random-nums` or set $PATH variable as follows:

        ```
        export PATH=$HOME/<location-for-above-executable>:$PATH  
        ```
3. Set execute permission to make utility executable :

        ```
        chmod 755 print-random-nums
        ```
4. To run the CLI utility from terminal on Linux or MacOS:

        ```
        print-random-nums
        ```
5. Will print 1 to 10 number in random order everytime on terminal.