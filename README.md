# pytrix
#### !!! does not work, won't be fixed !!! ####


# Configuration

## Version
#### !!! DO NOT CHANGE!!!
Version is internally used to check, if the config-file is up-to-date

## Update Url
Url of the Update repository to download / update the plugins from. Must point to a zip file which contains a folder 
`plugins` which contains the plugins, each in its own folder
* Type: `string`
* Default value: `https://github.com/Paul-Lukas/pytrix_plugins/archive/refs/heads/main.zip`

## use Simulation Gui

use Simulation instead of the Hardware Output

* Type: `boolean`
* Default value: `True`
* Options: `True`, `False`

## width

width of the Hardware/Gui output

* Type: `int`
* Default value: `15`

## height

height of the Hardware/Gui output

* Type: `int`
* Default value: `30`

## orientation

orientation and wiring type of the Hardware output

* Type: `int`
* Default value: `1`
* Options: `1`

_Different types (numbers are the indices on the rgb strip)_

Type 1:

| 1   | 8   | 9   |
|-----|-----|-----|
| 2   | 7   | 10  |
| 3   | 6   | 12  |
| 4   | 5   | 12  |
