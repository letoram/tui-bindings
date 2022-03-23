# Arcan python bindings

## Examples
First of all you need to start arcan console

- Clone and build https://github.com/letoram/arcan
- Start console
    ```bash
    
    ./arcan -w 640 -h 480 -T ../data/scripts -p ../data/resources ../data/appl/console
    ```
- Install the package:
    ```bash
    python setup.py install
    ```

### Clock
```bash
ARCAN_CONNPATH=console python examples/clock.py
```

### Listwnd
```bash
ARCAN_CONNPATH=console python examples/listwnd.py
```

### Bufferwnd
```bash
ARCAN_CONNPATH=console python examples/bufferwnd.py
```
