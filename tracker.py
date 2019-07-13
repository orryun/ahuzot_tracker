import requests
from argparse import ArgumentParser
from time import strftime
from re import compile


DATE_FORMAT = "%d/%m/%Y,%a,%H,%M"
URL = "http://www.ahuzot.co.il/Parking/ParkingDetails/"
ERROR = "Unknown"
STATUS_NAMES = {
	"panui": "Free",
	"meat": "Few",
	"male": "Full",
	"pail": "Active",
}
STATUS_REGEX = compile("pics/ParkingIcons/({})\.png".format("|".join(STATUS_NAMES.keys())))


def get_args() -> dict:
	args = ArgumentParser()
	args.add_argument("-p", "--parks", type=int, nargs="+", help="Ahuzot Park ID", required=True)
	return args.parse_args()


def get_park_status(park_id: int) -> int:
	resp = requests.get(URL, params={"ID": park_id})
	matches = STATUS_REGEX.findall(resp.text)
	if len(matches) > 0:
		return STATUS_NAMES.get(matches[0], ERROR)
	return ERROR


def main():
	args = get_args()
	park_status = ",".join([get_park_status(park) for park in args.parks])
	date = strftime(DATE_FORMAT)
	print(f"{date},{park_status}")


if __name__ == "__main__":
	main()
