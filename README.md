# Python Scripts

[![status](https://img.shields.io/badge/status-%20active%20development-red.svg)]()
[![lang](https://img.shields.io/badge/language-python%203-brightgreen.svg)]()
[![license](https://img.shields.io/badge/license-MIT%20-blue.svg)]()

## To Do:
Mayhaps add input file support with a flag.
Maybe save basic data to a file / graph because of a flag.

## Ideal Usage:
Give the command space delimited IPv4 addresses. It will return geo location data from and API (ip-api.com).

Ideal Input:

`geo 8.8.8.8 8.8.4.4`

Ideal Output:
```
----------
| IP:         8.8.8.8
| Country:    United States (US)
| Region:     California (CA)
| ISP:        Google
----------
| IP:         8.8.4.4
| Country:    United States (US)
| Region:     California (CA)
| ISP:        Level 3 Communications
----------
```
