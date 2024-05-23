# Icon Extract

This tiny project is aimed at extracting the icon from a Windows executable and converting it to an Apple Icon Image.

## Dependencies

The script relies on icoutils, which can be installed with `brew install icoutils`.

## Usage

1. Make the script executable

	```bash
	chmod +x icon-extract.py
	```

2. `icon-extract.py`

	```
	usage: icon-extract.py [-h] [-n NAME] [-o OUTPUT] inputfile

	Extract the icon from a Windows executable and convert it to an Apple Icon Image.
	Extract the icon from a Windows executable and convert it to an Apple Icon Image.

	positional arguments:
	inputfile             The executable to extract the icon from

	options:
	-h, --help            show this help message and exit
	-n NAME, --name NAME  The name of the icon
	-o OUTPUT, --output OUTPUT
							The output icon
	```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE.md) file for details.

---

Last Update: May 23, 2024


