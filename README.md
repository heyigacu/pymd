
# pymd
## Amber
### prepare system



### run system

#### continuous your MD (for case your MD task was accidentally shut down)

##### gamd
Unexpected interruption of gamd tasks is a huge problem, mainly because the gamd.log file is not written in sync with the trace file. Here we use interpolation to smooth out the missing gamd.log data.
```

bash nowat_continuous.sh
continuous.py
```


