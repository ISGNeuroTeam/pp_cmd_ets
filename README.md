# pp_cmd_ets
Postprocessing command "ets"

Usage example:
```
... | ets target_col='INDICATOR_VALUE', trend='add', periods=10, epoch_time=True"
```
## required parameters
- `target_col` - to specify the name of the data column
- `periods` - to specify amount of periods you want to get a forecast for
## optional parameters
- `time_col` - to specify the name of the datetime column. `_time` by default, if not set.
- `trend` - to specify trend model. It has only `add` option. `None` by default, if not set.
- `time_epoch` - if datetime format is in epoch format set this parameter to `True`: `time_epoch=True`
if you datetime format is usual - do not use this parameter at all.

## Getting started
###  Prerequisites
[Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Installing
1. Create virtual environment with post-processing sdk 
    ```
    bash
    make dev
    ```
    This command
        - creates python virtual environment with [postprocessing_sdk](https://github.com/ISGNeuroTeam/postprocessing_sdk)
        - creates `pp_cmd` directory with links to available post-processing commands
        - creates `otl_v1_config.ini` with otl platform address configuration

2. Configure connection to platform in `otl_v1_config.ini`

### Test ets
Use `pp` to test ets command:  
```
bash
pp
Storage directory is /tmp/pp_cmd_test/storage
Commmands directory is /tmp/pp_cmd_test/pp_cmd
query: | otl_v1 <# makeresults count=100 #> |  ets 
```
