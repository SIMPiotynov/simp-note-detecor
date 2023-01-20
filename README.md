# simp-note-detector

## Paquets necessaires
- mido (`pip3 install mido`)
- json (`pip3 install json`)

## Utilisation

- `-h, --help` : Affiche le message d'aide
- `-f, --file [chemin du fichier]` : Indique le fichier à convertir
- `-t, --type [arduino|rtttl]` : Le mode de conversion du fichier (arduino par defaut)

```
./convert -f fichier.mid -t rtttl
```