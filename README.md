# nsping
Nslookup and Ping on multiple entries

## Installation / Usage
Use the script nsping.py

```bash
python3 nsping.py list_of_entries.txt
```
## Source File
Your source file should have 1 entry per line, the entry can either be an IP address or a hostname:

```text
8.8.8.8
8.8.4.4
8.8.4.5
amazon.com
amaron.de
```
## Output File
The output is a CSV file, containing the following columns and separated by ";":
```csv
ID;Source;IP;Name;Ping
```
Where:
- ID: line position, based from source file
- Source: the entry as it was in the source file
- IP: the IP address, either found by nslookup based on the source (hostname) if hostname was provided, otherwise, IP address is equal to Source
- Hostname: hostname, either found by nslookup based on the source (IP) if IP was provided, otherwise, Name is equal to Source
- Ping: this bolean will return True, False, or NOT ATTEMPTED if we can't find the IP address of an host using nslookup, or if the IP address is not valid
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
