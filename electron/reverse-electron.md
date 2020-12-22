The electron executable is compressed archive so we can extract its contents with 7z for example on linux:

```bash
7z x santa-shop.exe
```

Once you cd into the newly extracted $PLUGINS/resources directory you will be presented with an app.asar. You can extract the contents used to build this asar package with the following:

```bash
sudo asar extract app.asar out-dir
```

This reveals an out-dir/main.js and other associated files used to build the application.

```bash
cat out-dir/main.js |grep PASSWORD

returns:

const SANTA_PASSWORD = 'santapass';
  return (password === SANTA_PASSWORD);
```
