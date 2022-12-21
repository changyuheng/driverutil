# driverutil

A Windows driver utility.

## Usage

### List SourceDiskFiles

```
driverutil source-disk-files <INF>
```

## Development

* Python 3.11+
* Hatch
* PyInstaller
* PyCharm

### Package

```shell
hatch run pyinstaller --clean --onefile --name driverutil --console Scripts/cli
```

The result will be located in the `dist` folder.
