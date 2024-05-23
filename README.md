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

	positional arguments:
		inputfile				The executable to extract the icon from

	options:
		-h, --help            	Show this help message and exit
		-n NAME, --name			The name of the icon
		-o OUTPUT, --output		The output icon								
	```

## License

This project is licensed under the GNU Lesser General Public License v3.0. See the [LICENSE](LICENSE.md) file for details.

---

Last Update: May 23, 2024


